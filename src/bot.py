import tweepy
import random
import time
from datetime import datetime
from config.settings import *
from src.utils.logger import setup_logger

class TwitterBot:
    def __init__(self):
        self.logger = setup_logger()
        self.logger.info("Initializing Twitter bot...")
        
        try:
            # Verify credentials are available
            if not all([TWITTER_BEARER_TOKEN, TWITTER_API_KEY, TWITTER_API_SECRET, 
                       TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
                raise ValueError("Missing required Twitter credentials")
            
            # Initialize client with both Bearer Token and OAuth 1.0a credentials
            self.client = tweepy.Client(
                bearer_token=TWITTER_BEARER_TOKEN,
                consumer_key=TWITTER_API_KEY,
                consumer_secret=TWITTER_API_SECRET,
                access_token=TWITTER_ACCESS_TOKEN,
                access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
                wait_on_rate_limit=True
            )
            
            # Test authentication
            self.logger.info("Testing authentication...")
            me = self.client.get_me()
            self.logger.info(f"Successfully authenticated as @{me[0].username}")
            
        except ValueError as e:
            self.logger.error(f"Configuration error: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Authentication failed: {str(e)}")
            raise

    def run(self):
        """Main method to run the Twitter bot"""
        self.logger.info("Starting Twitter bot...")
        
        try:
            # Get user ID
            user = self.client.get_me()[0]
            user_id = user.id
            self.logger.info(f"Bot user ID: {user_id}")
            
            # Initialize last_mention_id
            last_mention_id = None
            
            while True:
                try:
                    # Get mentions using v2 endpoint
                    self.logger.info("Checking for mentions...")
                    mentions = self.client.get_users_mentions(
                        id=user_id,
                        since_id=last_mention_id,
                        tweet_fields=['text', 'author_id', 'conversation_id'],
                        user_fields=['username'],
                        expansions=['author_id']
                    )
                    
                    if mentions.data:
                        for mention in mentions.data:
                            self.logger.info(f"Found mention: {mention.text}")
                            last_mention_id = mention.id
                    
                    time.sleep(60)  # Check every minute
                    
                except Exception as e:
                    self.logger.error(f"Error processing mentions: {str(e)}")
                    time.sleep(60)
                    
        except Exception as e:
            self.logger.error(f"Fatal error: {str(e)}")
            raise