# SentimentalAnalysis
# Twitter Sentiment Analysis Project
This project performs sentiment analysis on Twitter data, classifying tweets as either positive or negative. Using machine learning models—Naive Bayes, Random Forest, and Support Vector Machine (SVM)—the project aims to accurately determine sentiment in large social media datasets.

# Project Summary
The project leverages natural language processing (NLP) and machine learning to assess sentiment within tweets. Data preprocessing steps include removing URLs, mentions, and non-alphabet characters, followed by tokenization, lemmatization, and stopword removal. Three different models are applied, and hyperparameter tuning is conducted to optimize accuracy.

# Key Features
Data Cleaning and Preprocessing: Filters out irrelevant characters, URLs, and stopwords to prepare text data for analysis.
Machine Learning Models: Implements Naive Bayes, Random Forest, and SVM to classify tweet sentiment.
Hyperparameter Optimization: Uses Grid Search to fine-tune model parameters, enhancing classification accuracy.
Performance Evaluation: Analyzes models with metrics such as accuracy, precision, recall, and F1-score, along with ROC and precision-recall curves for visualization.
Results and Insights
The model achieved a high classification accuracy, with Random Forest and SVM showing strong performance after tuning. Visualizations illustrate the effectiveness of each model in classifying tweet sentiment.

# Technologies Used
Python and Scikit-learn for model implementation
NLTK for text preprocessing

