import pickle
from lime.lime_text import LimeTextExplainer
import numpy as np
import pandas as pd
from preprocessing import preprocess_text
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
matplotlib.rc('axes', titlesize=16)
matplotlib.rc('axes', labelsize=16)
matplotlib.rc('figure', titlesize=24)

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

    words = [item[0] for item in explanations_as_array]
    weights = [float(item[1]) for item in explanations_as_array]

    # Create the plot
    fig, ax = plt.subplots()

    for i in range(len(words) - 1, -1, -1):
        color = 'blue' if weights[i] >= 0 else 'orange'
        ax.barh(words[i], weights[i], color=color)

    ax.set_title('Influences of the words on the indicated feelings', fontsize=16)
    ax.set_xticklabels([])
    ax.set_xlim([-0.05, 0.05])

    legend_patches = [plt.Rectangle((0, 0), 1, 1, color='blue'), plt.Rectangle((0, 0), 1, 1, color='orange')]
    legend_labels = [prediction.capitalize(), 'Other Feelings']
    ax.legend(legend_patches, legend_labels, bbox_to_anchor=(1.05, 0.9), loc='center left')
    ax.axvline(0, color='black', linestyle='--')
    ax.text(-0.05, -1 // 2, 'Against ' + prediction.capitalize(), fontsize=14, rotation=0, va='center')
    ax.text(0.035, -1 // 2, 'Pro ' + prediction.capitalize(), fontsize=14, rotation=0, va='center')

    plt.savefig(figure_name, bbox_inches='tight')

    return prediction, explanations_as_array, category_prediction, sorted_category_proba
