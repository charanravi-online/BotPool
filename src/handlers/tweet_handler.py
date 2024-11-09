import random
from data.responses import RANDOM_TWEETS, HASHTAGS
from src.utils.logger import setup_logger

class TweetHandler:
    def __init__(self, client):
        self.client = client
        self.logger = setup_logger()

    def post_random_tweet(self):
        """Post a random tweet with hashtags"""
        tweet = random.choice(RANDOM_TWEETS)
        hashtags = ' '.join(random.sample(HASHTAGS, 2))
        full_tweet = f"{tweet}\n\n{hashtags}"
        
        try:
            response = self.client.create_tweet(text=full_tweet)
            self.logger.info(f"Posted tweet ID: {response.data['id']}")
            return response
        except Exception as e:
            self.logger.error(f"Error posting tweet: {e}")
            return None