from nltk.sentiment import SentimentIntensityAnalyzer
import nltk


sia = SentimentIntensityAnalyzer()


def SentimentAnalyzer(text):
    """True if tweet has positive compound sentiment, False otherwise."""
    return sia.polarity_scores(text)