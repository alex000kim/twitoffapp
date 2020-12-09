"""SQLAlchemy models and utility functions for TwitOff."""
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):
    """Twitter users corresponding to Tweets in the Tweet table."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String(15), nullable=False)
    # Tweet IDs are ordinal ints, so can be used to fetch only more recent
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f'<User {self.name}>'


class Tweet(DB.Model):
    """Tweets and their embeddings from Basilica."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))  # Allowing for full + links
    embedding = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f'<Tweet {self.text}>'