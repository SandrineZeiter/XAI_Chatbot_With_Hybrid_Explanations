import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
from preprocessing import preprocess_text
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv('balanced_dataset.csv')
data['text'] = data['text'].apply(preprocess_text)

X_train, X_test, y_train, y_test = train_test_split(data['text'], data['emotions'], test_size=0.2, random_state=42)

vectorizer = TfidfVectorizer(min_df=5, ngram_range=(1, 2), smooth_idf=True, use_idf=True)
vectorizer.fit(X_train)
X_train_tfidf = vectorizer.transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
mnb = MultinomialNB(alpha=2.75)
mnb.fit(X_train_tfidf, y_train)

y_pred_mnb = mnb.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred_mnb)

model_data = {
    'model': mnb,
    'vectorizer': vectorizer
}

file = open('my_mnb.pkl', 'wb')
pickle.dump(model_data, file)
