from telegram import ReplyKeyboardMarkup
import requests
from datetime import datetime
import csv

from questions_dict import questions
from credentials import *
import os

ids_chatnames = []
dict_id_input = {}
dict_id_notification = {}
dict_notification = {}
smiley = u'\U0001F60A'


def send_message(chat_id, text, reply_markup=None):
    url = f'{telegram_base_url}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': reply_markup
    }

    if reply_markup is not None:
        if isinstance(reply_markup, ReplyKeyboardMarkup):
            payload['reply_markup'] = reply_markup.to_json()

        else:
            payload['reply_markup'] = reply_markup

    requests.get(url, params=payload)


# Replacing user's keyboard with own button keyboard
def send_buttons(chat_id, question_nr):
    message = questions[question_nr]

    keyboard = [
        ['1', '2', '3', '4', '5']
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    send_message(chat_id, message, reply_markup=reply_markup)
    return message, reply_markup


def send_notification():
    check_status()
    for chat_id, chat_name in dict_notification.items():
        message = "Hi, {} {} I hope you had a great day! Could you please share how your day at work went and what " \
                  "tasks you worked on today?".format(chat_name, smiley)
        send_message(chat_id, message)

    for chat_id in dict_id_notification:
        dict_id_notification[chat_id][0] = True


# Check function to see what users must be notified at the scheduled time
def check_status():
    if len(dict_id_notification) != 0:
        for chat_id, notification in dict_id_notification.items():
            if notification[0]:
                dict_notification[chat_id] = notification[1]
            else:
                if chat_id in dict_notification:
                    del dict_notification[chat_id]


def create_file(chat_id, answer, userinput):
    now = datetime.now()
    current_time_str = now.strftime('%Y-%m-%d %H:%M:%S')
    current_date_str = now.strftime('%Y-%m-%d')

    chat_id_string = str(chat_id)
    file_name = 'Noxi_' + chat_id_string + '_' + current_date_str + '.csv'
    write_header = True
    header = ['User ID', 'Userinput', 'Current time', 'Answer', 'Explainability']
    check_status()

    if os.path.exists(file_name):
        write_header = False

    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerow([chat_id, userinput, current_time_str, answer, 'no'])

