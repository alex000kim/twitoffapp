"""Prediction of Users based on Tweet embeddings."""
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from .models import User
from .twitter import vectorize_tweet

def predict_user(user1_name, user2_name, tweet_text):
    """Determine and return which user is more likely to say a given Tweet."""
    user_set = pickle.dumps((user1_name, user2_name))  # users are sorted
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    # X matrix of features
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    # y array of labels
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])

    knnc = KNeighborsClassifier(weights='distance', metric='cosine').fit(embeddings, labels)
    #vectorizing the tweet using spacy
    tweet_embedding = vectorize_tweet(tweet_text)
    prediction = knnc.predict(np.array(tweet_embedding).reshape(1, -1)) # will return 1 for user1 or 0 or user2
    return prediction