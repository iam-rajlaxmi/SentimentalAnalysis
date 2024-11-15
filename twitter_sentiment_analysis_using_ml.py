# -*- coding: utf-8 -*-
"""Twitter Sentiment Analysis using ML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HFeuMRGWzfXInpv7QCxifTTAYFeiadPC
"""

# @title
#installing kaggle library
!pip install kaggle



# uploading kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

# API to fetch dataset from kaggle
!kaggle datasets download -d kazanova/sentiment140

# extracting the compressed dataset
from zipfile import ZipFile
dataset = '/content/sentiment140.zip'

with ZipFile(dataset, 'r') as zip:
   zip.extractall()
   print('The dataset is extracted')

# Importing necessary libraries
# import numpy as np
# import pandas as pd
# import re
# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# # Import the necessary libraries
# from sklearn.model_selection import GridSearchCV  # Import GridSearchCV from sklearn.model_selection
# from sklearn.linear_model import LogisticRegression # Import Logistic Regression model
# from sklearn.model_selection import train_test_split # Import train_test_split for data splitting

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import pickle

# # Download stopwords and WordNet corpus
# nltk.download('stopwords')
# nltk.download('wordnet')
# Download stopwords and WordNet corpus
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# # Function to preprocess the text data
# def preprocess_text(content):
#     # Remove URLs, mentions, and hashtags
#     content = re.sub(r"http\S+|www\S+|https\S+", '', content, flags=re.MULTILINE)
#     content = re.sub(r'\@\w+|\#','', content)

#     # Remove non-alphabetical characters
#     content = re.sub('[^a-zA-Z]', ' ', content)

#     # Convert to lowercase
#     content = content.lower()

#     # Tokenize, remove stopwords, and lemmatize
#     content = content.split()
#     content = [lemmatizer.lemmatize(word) for word in content if word not in stopwords.words('english')]

#     # Join back into a single string
#     content = ' '.join(content)
#     return content

# Function to preprocess the text data
def preprocess_text(content):
    # Remove URLs, mentions, and hashtags
    content = re.sub(r"http\S+|www\S+|https\S+", '', content, flags=re.MULTILINE)
    content = re.sub(r'\@\w+|\#','', content)

    # Remove non-alphabetical characters
    content = re.sub('[^a-zA-Z]', ' ', content)

    # Convert to lowercase
    content = content.lower()

    # Tokenize, remove stopwords, and lemmatize
    content = content.split()
    content = [lemmatizer.lemmatize(word) for word in content if word not in stopwords.words('english')]

    # Join back into a single string
    content = ' '.join(content)
    return content

# # Load the dataset
# twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1', names=['target', 'id', 'date', 'flag', 'user', 'text'])

# Load the dataset
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1', names=['target', 'id', 'date', 'flag', 'user', 'text'])

# # Apply preprocessing
# twitter_data['cleaned_text'] = twitter_data['text'].apply(preprocess_text)
# Apply preprocessing
# twitter_data['cleaned_text'] = twitter_data['text'].apply(preprocess_text)
#  Sample 10% of data for faster processing
twitter_data = twitter_data.sample(frac=0.1, random_state=42)

import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, precision_recall_curve

# Visualize the distribution of the target variables
# Count the number of positive and negative tweets
target_counts = twitter_data['target'].replace(4, 1).value_counts()
labels = ['Negative', 'Positive']

# Bar Chart for Target Variable Distribution
plt.figure(figsize=(6, 4))
plt.bar(labels, target_counts, color=['red', 'green'])
plt.xlabel('Sentiment')
plt.ylabel('Number of Tweets')
plt.title('Distribution of Sentiment in Dataset')
plt.show()

# # Define the target variable
# Y = twitter_data['target'].replace(4, 1).values  # Replace '4' with '1' for binary classification (positive = 1, negative = 0)

# Define the target variable
Y = twitter_data['target'].replace(4, 1).values  # Replace '4' with '1' for binary classification (positive = 1, negative = 0)

# # Use TfidfVectorizer with optimized parameters
# from sklearn.feature_extraction.text import TfidfVectorizer
# vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
# X = vectorizer.fit_transform(twitter_data['cleaned_text'])

# Use TfidfVectorizer with optimized parameters
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X = vectorizer.fit_transform(twitter_data['cleaned_text'])

# # Splitting data into training and test sets
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# Splitting data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# # Define the Logistic Regression model
# model = LogisticRegression()

# Define the SVM model
svm_model = SVC()

"""convert the target "4" to "1"
"""

# # Set up Grid Search for hyperparameter tuning
# param_grid = {
#     'C': [0.1, 1, 10],
#     'max_iter': [100, 200, 300]
# }


# # Set up Grid Search for hyperparameter tuning
# param_grid = {
#     'C': [0.1, 1, 10],
#     'kernel': ['linear', 'rbf'],
#     'gamma': ['scale', 'auto']
# }

# Set up Grid Search for hyperparameter tuning
param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto']
}

# # Perform Grid Search
# grid_search = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
# grid_search.fit(X_train, Y_train)

# Perform Grid Search
grid_search = GridSearchCV(svm_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, Y_train)

"""0---> negative tweet
1---> positive tweet

Stemming

Stemming is the process of reducing a word to its Root word

example: actor,actress,acting = act
"""

# # Use the best model from Grid Search
# best_model = grid_search.best_estimator_

# Use the best model from Grid Search
best_model = grid_search.best_estimator_

# # Training Accuracy
# train_accuracy = best_model.score(X_train, Y_train)
# print("Training Accuracy: ", train_accuracy)

# Training Accuracy
train_accuracy = best_model.score(X_train, Y_train)
print("SVM Training Accuracy: ", train_accuracy)

# # Testing Accuracy
# test_accuracy = best_model.score(X_test, Y_test)
# print("Test Accuracy: ", test_accuracy)

# Testing Accuracy
test_accuracy = best_model.score(X_test, Y_test)
print("SVM Test Accuracy: ", test_accuracy)

# # Save the best model and vectorizer
# import pickle
# pickle.dump(best_model, open('best_model.sav', 'wb'))
# pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))

# Save the best model and vectorizer
pickle.dump(best_model, open('best_svm_model.sav', 'wb'))
pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))

# # Load the model and vectorizer
# loaded_model = pickle.load(open('best_model.sav', 'rb'))
# loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

# Load the model and vectorizer
loaded_model = pickle.load(open('best_svm_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

# Visualization 1: Confusion Matrix
y_pred = loaded_model.predict(X_test)
cm = confusion_matrix(Y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# Visualization 2: Training vs. Test Accuracy
accuracies = [train_accuracy, test_accuracy]
labels = ['Training Accuracy', 'Test Accuracy']
plt.figure(figsize=(6,4))
plt.bar(labels, accuracies, color=['blue', 'green'])
plt.ylim(0, 1)  # Set y-axis limit to [0, 1]
plt.ylabel('Accuracy')
plt.title('Training vs. Test Accuracy')
plt.show()

# Visualization 3: ROC Curve
y_scores = best_model.decision_function(X_test)
fpr, tpr, _ = roc_curve(Y_test, y_scores)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Diagonal line
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()

# Visualization 4: Precision-Recall Curve
precision, recall, _ = precision_recall_curve(Y_test, y_scores)
plt.figure(figsize=(6, 4))
plt.plot(recall, precision, color='blue', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True)
plt.show()

# # Example prediction
# X_new_text = twitter_data['text'][200]  # Use the original text data for prediction
# print('Actual:', Y_test[200])

# Example prediction
X_new_text = twitter_data['text'][200]  # Use the original text data for prediction
print('Actual:', Y_test[200])

# # Transform the new text using the loaded vectorizer
# X_new_transformed = loaded_vectorizer.transform([X_new_text])

# Transform the new text using the loaded vectorizer
X_new_transformed = loaded_vectorizer.transform([X_new_text])

# # Predict using the loaded model
# prediction = loaded_model.predict(X_new_transformed)

# if prediction[0] == 0:
#     print('Negative Tweet')
# else:
#     print('Positive Tweet')


# Predict using the loaded model
prediction = loaded_model.predict(X_new_transformed)

if prediction[0] == 0:
    print('Negative Tweet')
else:
    print('Positive Tweet')

# # Another example prediction
# X_new_text_2 = twitter_data['text'][3]
# print('Actual:', Y_test[3])

# # Transform the new text using the loaded vectorizer
# X_new_transformed_2 = loaded_vectorizer.transform([X_new_text_2])

# # Predict using the loaded model
# prediction_2 = loaded_model.predict(X_new_transformed_2)

# if prediction_2[0] == 0:
#     print('Negative Tweet')
# else:
#     print('Positive Tweet')



# Another example prediction
X_new_text_2 = twitter_data['text'][3]
print('Actual:', Y_test[3])

# Transform the new text using the loaded vectorizer
X_new_transformed_2 = loaded_vectorizer.transform([X_new_text_2])

# Predict using the loaded model
prediction_2 = loaded_model.predict(X_new_transformed_2)

if prediction_2[0] == 0:
    print('Negative Tweet')
else:
    print('Positive Tweet')

# Installing kaggle library
!pip install kaggle
# uploading kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
# API to fetch dataset from kaggle
!kaggle datasets download -d kazanova/sentiment140
# extracting the compressed dataset
from zipfile import ZipFile
dataset = '/content/sentiment140.zip'

with ZipFile(dataset, 'r') as zip:
   zip.extractall()
   print('The dataset is extracted')

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Download stopwords and WordNet corpus
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize Lemmatizer
lemmatizer = WordNetLemmatizer()

# Function to preprocess the text data
def preprocess_text(content):
    # Remove URLs, mentions, and hashtags
    content = re.sub(r"http\S+|www\S+|https\S+", '', content, flags=re.MULTILINE)
    content = re.sub(r'\@\w+|\#','', content)

    # Remove non-alphabetical characters
    content = re.sub('[^a-zA-Z]', ' ', content)

    # Convert to lowercase
    content = content.lower()

    # Tokenize, remove stopwords, and lemmatize
    content = content.split()
    content = [lemmatizer.lemmatize(word) for word in content if word not in stopwords.words('english')]

    # Join back into a single string
    content = ' '.join(content)
    return content


# Load the dataset
twitter_data = pd.read_csv('/content/training.1600000.processed.noemoticon.csv', encoding='ISO-8859-1', names=['target', 'id', 'date', 'flag', 'user', 'text'])

# Sample 10% of data for faster processing
twitter_data = twitter_data.sample(frac=0.1, random_state=42)

# Preprocess the text column
twitter_data['cleaned_text'] = twitter_data['text'].apply(preprocess_text)

# Define the target variable
Y = twitter_data['target'].replace(4, 1).values  # Replace '4' with '1' for binary classification (positive = 1, negative = 0)

# Use TfidfVectorizer with optimized parameters
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X = vectorizer.fit_transform(twitter_data['cleaned_text'])

# Splitting data into training and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# Define the Random Forest model
rf_model = RandomForestClassifier(random_state=42)

# Set up Grid Search for hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10]
}

# Perform Grid Search
grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, Y_train)

# Use the best model from Grid Search
best_model = grid_search.best_estimator_

# Training Accuracy
train_accuracy = best_model.score(X_train, Y_train)
print("Random Forest Training Accuracy: ", train_accuracy)

# Testing Accuracy
test_accuracy = best_model.score(X_test, Y_test)
print("Random Forest Test Accuracy: ", test_accuracy)

# Save the best model and vectorizer
pickle.dump(best_model, open('best_rf_model.sav', 'wb'))
pickle.dump(vectorizer, open('vectorizer.sav', 'wb'))

# Load the model and vectorizer
loaded_model = pickle.load(open('best_rf_model.sav', 'rb'))
loaded_vectorizer = pickle.load(open('vectorizer.sav', 'rb'))

# Visualization 1: Confusion Matrix
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, precision_recall_curve
import matplotlib.pyplot as plt

y_pred = loaded_model.predict(X_test)
cm = confusion_matrix(Y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Negative', 'Positive'])
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# Visualization 2: Training vs. Test Accuracy
accuracies = [train_accuracy, test_accuracy]
labels = ['Training Accuracy', 'Test Accuracy']
plt.figure(figsize=(6,4))
plt.bar(labels, accuracies, color=['blue', 'green'])
plt.ylim(0, 1)  # Set y-axis limit to [0, 1]
plt.ylabel('Accuracy')
plt.title('Training vs. Test Accuracy')
plt.show()

# Visualization 3: ROC Curve
y_scores = best_model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(Y_test, y_scores)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(6, 4))
plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')  # Diagonal line
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC)')
plt.legend(loc="lower right")
plt.show()

# Visualization 4: Precision-Recall Curve
precision, recall, _ = precision_recall_curve(Y_test, y_scores)
plt.figure(figsize=(6, 4))
plt.plot(recall, precision, color='blue', lw=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision-Recall Curve')
plt.grid(True)
plt.show()

# Example prediction
X_new_text = twitter_data['text'][200]  # Use the original text data for prediction
print('Actual:', Y_test[200])

# Transform the new text using the loaded vectorizer
X_new_transformed = loaded_vectorizer.transform([X_new_text])

# Predict using the loaded model
prediction = loaded_model.predict(X_new_transformed)

if prediction[0] == 0:
    print('Negative Tweet')
else:
    print('Positive Tweet')