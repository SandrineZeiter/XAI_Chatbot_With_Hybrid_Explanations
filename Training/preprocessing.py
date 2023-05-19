import re
import string

from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords


def contraction(text):
    words = text.split()

    for i in range(len(words)):
        if "'" in words[i]:
            words[i] = words[i].replace("'", "")
    return " ".join(words)


def negation_handling(text):
    words = word_tokenize(text)
    negation = False
    result = []
    for word in words:
        if negation:
            result.append("NOT_" + word)
        else:
            result.append(word)
        if word in ["not", "n't", "no", "never", "nothing"]:
            negation = True
        elif word in [".", "!", "?"]:
            negation = False
    return " ".join(result)


def preprocess_text(text):
    # Replace contractions with their expanded forms
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"n't", " not", text)
    text = re.sub(r"'re", " are", text)
    text = re.sub(r"'s", " is", text)
    text = re.sub(r"'d", " would", text)
    text = re.sub(r"'ll", " will", text)
    text = re.sub(r"'t", " not", text)
    text = re.sub(r"'ve", " have", text)

    text = text.lower()

    sentences = sent_tokenize(text)
    processed_sentences = []
    for sentence in sentences:
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = negation_handling(sentence)
        sentence = contraction(sentence)
        words = sentence.split()
        words = [word for word in words if word not in stopwords.words('english')]
        processed_sentence = ' '.join(words)
        processed_sentences.append(processed_sentence)
    processed_text = ' '.join(processed_sentences)
    return processed_text
