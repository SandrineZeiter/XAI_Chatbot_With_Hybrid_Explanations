import pickle
from lime.lime_text import LimeTextExplainer
import numpy as np
import pandas as pd
from preprocessing import preprocess_text


file = open('my_mnb.pkl', 'rb')
model_data = pickle.load(file)
data = pd.read_csv('balanced_dataset.csv')
class_names = ['anger', 'fear', 'joy', 'love', 'sadness', 'surprise']

mnb = model_data['model']
vectorizer = model_data['vectorizer']

explainer = LimeTextExplainer(class_names=class_names)


# Create the prediction function using MNB
def prediction_fn(text):
    text_vec = vectorizer.transform(text)
    pred = mnb.predict_proba(text_vec)
    return pred


def lime_testing_userinput(userinput, figure_name):
    preprocessed_userinput = preprocess_text(userinput)
    # Create the explainer
    exp = explainer.explain_instance(preprocessed_userinput,
                                     prediction_fn,
                                     num_features=5,
                                     top_labels=len(class_names))

    class_index = exp.available_labels()[0]
    prediction = class_names[class_index]

    # Get the explanations
    explanations = exp.as_list(label=class_index)
    explanations_as_array = np.array(explanations)

    category_proba = []
    probas = exp.predict_proba
    for i in range(len(class_names)):
        category_proba.append([class_names[i], round(probas[i], 2)])

    sorted_category_proba = sorted(category_proba, key=lambda x: x[1], reverse=True)

    pos_category_prediction = sum(category_proba[i][1] for i in [2, 3])
    neg_category_prediction = sum(category_proba[i][1] for i in [0, 1, 4])

    category_prediction_value = pos_category_prediction - neg_category_prediction

    # Define the categories
    if -1 <= category_prediction_value < -0.6:
        category_prediction = 'bad'
    elif -0.6 <= category_prediction_value < -0.2:
        category_prediction = 'rather bad'
    elif -0.2 <= category_prediction_value < 0.2:
        category_prediction = 'average'
    elif 0.2 <= category_prediction_value < 0.6:
        category_prediction = 'rather good'
    elif 0.6 <= category_prediction_value <= 1:
        category_prediction = 'good'

    return prediction, explanations_as_array, category_prediction, sorted_category_proba
