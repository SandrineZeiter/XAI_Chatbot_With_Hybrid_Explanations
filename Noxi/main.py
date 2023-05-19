from flask import Flask, request, jsonify
import telegram
import datetime
from datetime import timedelta, time
from apscheduler.schedulers.background import BackgroundScheduler

from messaging import *
from reaction_efficiency import *
from reaction_supervisor import *
from reaction_finishing import *
from reaction_interest import *
from reaction_concentration import *
from reaction_control import *
from categories import *

from lime_prediction import *
import json

global bot
global TOKEN

text_to_analyze = ' '
name = ' '
execution_time = 0
fulfillment_text = ''
chat_ids = set()
user_names = set()
id_counter_dictionary = {}
id_value_dictionary = {}
id_rating_dictionary = {}
id_prediction_dictionary = {}
start = ''
job_added = False

chatnames_ids = ids_chatnames
id_input_dictionary = dict_id_input
id_notification_dictionary = dict_id_notification

notification = False
# Change the TOKEN in credentials.py
TOKEN = telegram_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

# Schedule message to be sent daily
message_scheduler = BackgroundScheduler(daemon=True)
time_threshold = time(17, 52)
start_date = datetime.now().replace(hour=time_threshold.hour, minute=time_threshold.minute)
end_date = start_date + timedelta(days=7)

message_scheduler.add_job(send_notification,
                          'interval', days=1, start_date=start_date, end_date=end_date,
                          max_instances=1)
message_scheduler.start()


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    global text_to_analyze
    global name
    global execution_time
    global fulfillment_text
    global chat_ids
    global user_names
    global chatnames_ids
    global id_input_dictionary
    global notification
    global id_counter_dictionary
    global start
    emoji = u'\U0001F60A'

    now = datetime.now()
    current_time_str_filename = now.strftime('%Y-%m-%d_%H-%M-%S')

    time_threshold = time(17, 52)

    fulfillment_text = ''

    req = request.get_json()
    if not req:
        return jsonify({'status': 'error', 'message': 'Empty request'})

    query_result = req.get('queryResult')
    action = query_result.get('action')

    # Extract the needed data from the JSON file from Dialogflow
    if "from" in req.get('originalDetectIntentRequest').get('payload').get('data'):
        chat_name = req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('first_name')
        chat_id = req.get('originalDetectIntentRequest').get('payload').get('data').get('from').get('id')
    else:
        chat_name = req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get(
            'from').get('first_name')
        chat_id = req.get('originalDetectIntentRequest').get('payload').get('data').get('callback_query').get(
            'from').get('id')

    if chat_name not in user_names:
        user_names.add(chat_name)
        if chat_id not in chat_ids:
            chat_ids.add(chat_id)
            chatnames_ids.append([chat_name, chat_id])
            id_counter_dictionary[chat_id] = 2
            id_notification_dictionary[chat_id] = [True, chat_name]

    if now.time() < time_threshold:
        id_notification_dictionary[chat_id] = [False, chat_name]
    else:
        id_notification_dictionary[chat_id] = [True, chat_name]

    # Action detection of the Dialogflow intent
    if action == 'welcome':
        userinput = query_result.get('queryText')
        answer = 'Hello again, {} {} I hope you had a great day! Could you please share how your day at ' \
                 'work went and what tasks you worked on today?'.format(chat_name, emoji)
        id_counter_dictionary[chat_id] = 2
        send_message(chat_id, answer)
        create_file(chat_id, answer, userinput)
        res = {}

    elif action == 'button_number':
        userinput = query_result.get('queryText')
        int_number = ['1', '2', '3', '4', '5']
        # To make sure that the number is from a button
        if query_result.get('queryText') not in int_number:
            action = 'information'

        else:
            number_string = query_result.get('queryText')
            number = int(number_string)

            # Calculating the personal rating
            if chat_id not in id_value_dictionary:
                id_value_dictionary[chat_id] = number

            else:
                user_number = id_value_dictionary[chat_id]
                if id_counter_dictionary[chat_id] % 2 != 0:
                    user_number += number
                else:
                    user_number -= number
                id_value_dictionary[chat_id] = user_number

            number_index_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}

            # Creating a personalized answer using the input number
            if id_counter_dictionary[chat_id] in [3, 4, 5, 6, 7, 8]:
                # Use a dictionary to map id_counter_dictionary values to answer_dict
                answer_dict = {3: answers_efficiency, 4: answers_interest, 5: answers_control, 6: answers_finishing,
                               7: answers_supervisor, 8: answers_concentration}[id_counter_dictionary[chat_id]]

            if number in number_index_map:
                length = len(answer_dict[number_index_map[number]]) - 1
                answer_nr = random.randint(0, length)
                answer = answer_dict[number_index_map[number]][answer_nr]
                create_file(chat_id, answer, userinput)

            else:
                answer = 'Something went wrong. Please click again.'
                create_file(chat_id, answer, userinput)

            send_message(chat_id, answer)
            res = {}

    # Main calculations
    if action == 'information':
        userinput = query_result.get('queryText')
        original_request = req.get('originalDetectIntentRequest').get('payload').get('data')

        if 'entities' in original_request:
            start = original_request.get('entities')[0]['type']
            userinput = ''

        # Creating the very first conversation
        if start == 'bot_command':
            answer = 'Hi {}, I am Noxi {} Thank you for participating in this experiment. We will talk daily ' \
                     'until the end of the week. It would be nice to hear from you. However, if you do not initiate ' \
                     'conversation, I will be the one contacting you. ' \
                     '\n\nI would like to get to know you better to make some analysis. Thus, the more you say, the ' \
                     'better I can analyze you. So, let us start with the experiment.' \
                     '\n\n{}, I am curious to know more about your work today. Could you share some details about ' \
                     'what you were engaged in and what tasks you accomplished?' \
                .format(chat_name, emoji, chat_name)
            start = ''
            id_counter_dictionary[chat_id] = 2
            send_message(chat_id, answer)
            create_file(chat_id, answer, userinput)

            if chat_id not in id_input_dictionary:
                id_input_dictionary[chat_id] = userinput
                text_to_analyze += ' ' + userinput

        else:
            if chat_id not in id_input_dictionary:
                id_input_dictionary[chat_id] = userinput
                text_to_analyze += ' ' + userinput

            else:
                text_to_analyze = id_input_dictionary[chat_id]
                text_to_analyze += ' ' + userinput
                id_input_dictionary[chat_id] = text_to_analyze

            if id_counter_dictionary[chat_id] == 1:
                answer = 'Hi {}, I hope you had a great day!{} Could you please share how your day at work went and ' \
                         'what tasks you worked on today?'.format(chat_name, emoji)
                send_message(chat_id, answer)
                create_file(chat_id, answer, userinput)
                id_counter_dictionary[chat_id] += 1

            elif 2 <= id_counter_dictionary[chat_id] <= 7:
                send_buttons(chat_id, id_counter_dictionary[chat_id] - 1)
                answer = questions[id_counter_dictionary[chat_id]-1]
                create_file(chat_id, answer, userinput)
                id_counter_dictionary[chat_id] += 1

            # Creating the analysis and the feedback
            else:
                answer = "Thank you {} for sharing {} I will now quickly analyze what you've told me and provide you " \
                         "with feedback in just a moment.".format(chat_name, emoji)
                send_message(chat_id, answer)
                create_file(chat_id, answer, userinput)

                for category, value_range in category_ranges:
                    if id_value_dictionary[chat_id] in value_range:
                        # Define category for personal rating
                        id_rating_dictionary[chat_id] = [category, categories[category]]

                chat_id_string = str(chat_id)
                figure_name = 'Figure_' + chat_id_string + '_' + current_time_str_filename + '.png'
                # Using LIME for the predictions
                prediction, explanations, category_prediction, sorted_category_proba = \
                    lime_testing_userinput(text_to_analyze, figure_name)

                # Define category for predicted rating
                id_prediction_dictionary[chat_id] = [category_prediction, categories[category_prediction]]

                # Creating the answer if two feelings are rated too similarly
                if sorted_category_proba[0][1] - sorted_category_proba[1][1] < 0.05:
                    unsure_answer = "Upon reviewing your feedback on today's workday, I noticed that I rated two " \
                                    "feelings very similarly: {} with {}% and {} with {}%." \
                        .format(sorted_category_proba[0][0].upper(), 100 * sorted_category_proba[0][1],
                                sorted_category_proba[1][0].upper(), 100 * sorted_category_proba[1][1])
                else:
                    unsure_answer = "Furthermore, I would say, your feeling for today's workday is {}." \
                        .format(prediction.upper())

                # Comparing the personal rating and the predicted rating
                if id_rating_dictionary[chat_id][1] > id_prediction_dictionary[chat_id][1]:
                    answer_comparison = "{}, it seems that there might be a slight difference in our evaluations of " \
                                        "your workday. Based on the explanations you provided, you rated your " \
                                        "workday as {}, while I might have rated it lower, perhaps as {}. \n" \
                                            .format(chat_name,
                                                    id_rating_dictionary[chat_id][0].upper(),
                                                    id_prediction_dictionary[chat_id][0].upper(),
                                                    ) + unsure_answer

                elif id_rating_dictionary[chat_id][1] == id_prediction_dictionary[chat_id][1]:
                    answer_comparison = "{}, my analysis shows, that we both rate your workday similarly, " \
                                        "namely {}. \n" \
                                            .format(chat_name,
                                                    id_rating_dictionary[chat_id][0].upper()) + unsure_answer

                elif id_rating_dictionary[chat_id][1] < id_prediction_dictionary[chat_id][1]:
                    answer_comparison = "{}, it seems that you are being a bit harder on yourself than I would be. " \
                                        "Your rating of today's workday is {}, whereas my analysis would rate it as " \
                                        "{}. " \
                                            .format(chat_name,
                                                    id_rating_dictionary[chat_id][0].upper(),
                                                    id_prediction_dictionary[chat_id][0].upper()) + unsure_answer

                answer = answer_comparison

                if id_prediction_dictionary[chat_id][1] <= 2:
                    answer += '\n\nThank you for your time, {}. I hope you will have a better rest of the day'. \
                        format(chat_name)
                else:
                    answer += ' \n\nThank you for your time, {}. I wish you a wonderful day and see you next time {}'. \
                        format(chat_name, emoji)

                create_file(chat_id, answer, userinput)

                text_to_analyze = ''
                del id_input_dictionary[chat_id]
                del id_value_dictionary[chat_id]

                send_message(chat_id, answer)
                id_counter_dictionary[chat_id] = 2

        res = {}

    req_json = json.dumps(req)
    req_file = open('data.json', 'w')
    req_file.write(req_json)
    req_file.close()

    return jsonify(res)


if __name__ == '__main__':
    # Running the app on a different port than Chatty
    app.run(port=5001)

