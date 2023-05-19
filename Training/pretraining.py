import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

from preprocessing import preprocess_text

data = pd.read_csv('balanced_dataset.csv')
data['text'] = data['text'].apply(preprocess_text)

X_train, X_test, y_train, y_test = train_test_split(data['text'], data['emotions'], test_size=0.2, random_state=42)

tfidf = TfidfVectorizer(min_df=5, ngram_range=(1, 2), smooth_idf=True, use_idf=True)
tfidf.fit(X_train)
X_train_tfidf = tfidf.transform(X_train)
X_test_tfidf = tfidf.transform(X_test)


# Defining the parameter grid for grid search
alpha = np.arange(0, 10.5, 0.5)
param_grid = {'alpha': [2.74, 2.745, 2.75, 2.755, 2.76]}

# Creating a Multinomial Naive Bayes classifier
mnb = MultinomialNB()

grid_search = GridSearchCV(mnb, param_grid, cv=5, scoring='accuracy', return_train_score=True)

# Fitting the grid search object to the training data
grid_search.fit(X_train_tfidf, y_train)

# Printing the best parameters and best score
print("Best Parameters:", grid_search.best_params_)
print("Best Score:", grid_search.best_score_)

# Getting the predicted labels on the test data using the best estimator from the grid search
y_pred_mnb = grid_search.best_estimator_.predict(X_test_tfidf)
print(classification_report(y_test, y_pred_mnb))

