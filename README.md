# XAI_Chatbot_With_Hybrid_Explanations

**Master's Thesis: eXplainable AI - A Chatbot With Hybrid Explanations: Impact on User Perceptions and Behavior Within Different Groups**

This project is part of a master's thesis titled eXplainable AI - A Chatbot With Hybrid Explanations: Impact on User Perceptions and Behavior Within Different Groups"The purpose of this project is to create an XAI chatbot using LIME and to compare it to a non-explanatory chatbot.

## Folders

The project is organized into the following folders:

1. **Chatty**: The XAI chatbot
   - .gitignore
   - balanced_dataset.csv
   - categories.py
   - credentials.py
   - lime_prediction.py
   - main.py
   - messaging.py
   - my_mnb.pkl
   - preprocessing.py
   - Procfile
   - questions_dict.py
   - reaction_concentration.py
   - reaction_control.py
   - reaction_efficiency.py
   - reaction_finishing.py
   - reaction_interest.py
   - reaction_supervisor.py
   - requirements.txt

2. **Noxi**: The non-explanatory chatbot
   - balanced_dataset.csv
   - categories.py
   - credentials.py
   - lime_prediction.py
   - main.py
   - messaging.py
   - my_mnb.pkl
   - preprocessing.py
   - questions_dict.py
   - reaction_concentration.py
   - reaction_control.py
   - reaction_efficiency.py
   - reaction_finishing.py
   - reaction_interest.py
   - reaction_supervisor.py
   - requirements.txt

3. **Training**: Creating the ML model using MNB
   - balanced_dataset.csv
   - changing_dataset.py
   - dataset.csv
   - dataset_sorted.csv
   - main.py
   - my_mnb.pkl
   - preprocessing.py
   - pretraining.py

## Instructions

To use this project, please follow these steps:

1. Clone the repository to your local machine.
2. Open the `credentials.py` file located in Chatty and Noxi.
3. Adjust the Telegram token in the `credentials.py` file by replacing `ADD YOUR TELEGRAM TOKEN HERE` with your own token.
4. Save the `credentials.py` file after making the necessary changes.

## Usage

To use the bots you first have to create your own chatbots on `Dialogflow` (https://dialogflow.cloud.google.com). This bot should contain two intents named `welcome` and `button_number`, as well as a fallback-intent named `information`. Enable the webhook call for all three intents.

Then create a webhook. This can be done using `ngrok` (https://ngrok.com). This webhook should then be connected to `Dialogflow` in the `Fullfilment` section of `Dialogflow` where the webhook is enabled. 


