import tweepy
import random
import time
from datetime import datetime, timedelta
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
            
            # Initialize last_mention_id and last_check_time
            last_mention_id = None
            last_check_time = datetime.now()
            check_interval = 180  # Check every 3 minutes instead of every minute
            
            while True:
                try:
                    current_time = datetime.now()
                    # Only check if enough time has passed
                    if (current_time - last_check_time).seconds >= check_interval:
                        self.logger.info("Checking for mentions...")
                        
                        # Get mentions using v2 endpoint with pagination
                        mentions = self.client.get_users_mentions(
                            id=user_id,
                            since_id=last_mention_id,
                            tweet_fields=['text', 'author_id', 'conversation_id'],
                            user_fields=['username'],
                            expansions=['author_id'],
                            max_results=10  # Limit results per request
                        )
                        
                        if mentions.data:
                            for mention in mentions.data:
                                self.logger.info(f"Found mention: {mention.text}")
                                last_mention_id = mention.id
                                # Add a small delay between processing each mention
                                time.sleep(2)
                        
                        last_check_time = current_time
                        self.logger.info(f"Next check in {check_interval} seconds")
                    
                    # Sleep for a shorter interval to be more responsive
                    time.sleep(10)
                    
                except tweepy.errors.TooManyRequests as e:
                    # Handle rate limit explicitly
                    reset_time = int(e.response.headers.get('x-rate-limit-reset', 0))
                    wait_time = max(reset_time - time.time(), 0)
                    self.logger.warning(f"Rate limit reached. Waiting {int(wait_time)} seconds")
                    time.sleep(wait_time + 1)
                    
                except tweepy.errors.TwitterServerError as e:
                    self.logger.error(f"Twitter server error: {str(e)}")
                    time.sleep(60)
                    
                except Exception as e:
                    self.logger.error(f"Error processing mentions: {str(e)}")
                    time.sleep(60)
                    
        except Exception as e:
            self.logger.error(f"Fatal error: {str(e)}")
            raise

    def get_rate_limit_status(self):
        """Get current rate limit status"""
        try:
            # Get rate limit status for mentions endpoint
            response = self.client.rate_limit_status()
            mentions_limit = response['resources']['mentions']['/mentions/timeline']
            
            self.logger.info(f"Rate Limit Status:")
            self.logger.info(f"Remaining: {mentions_limit['remaining']}")
            self.logger.info(f"Limit: {mentions_limit['limit']}")
            self.logger.info(f"Reset Time: {datetime.fromtimestamp(mentions_limit['reset'])}")
            
            return mentions_limit
            
        except Exception as e:
            self.logger.error(f"Error getting rate limit status: {str(e)}")
            return None