import random
from data.responses import FUNNY_RESPONSES
from src.utils.logger import setup_logger

class ReplyHandler:
    def __init__(self, client):
        self.client = client
        self.logger = setup_logger()

    def process_mentions(self):
        """Process and reply to mentions"""
        try:
            # Get authenticated user's ID
            user = self.client.get_me()
            user_id = user.data.id
            
            # Get mentions
            mentions = self.client.get_users_mentions(
                id=user_id,
                expansions=['author_id'],
                tweet_fields=['conversation_id']
            )
            
            if mentions.data:
                for mention in mentions.data:
                    self._reply_to_mention(mention)
                    
        except Exception as e:
            self.logger.error(f"Error processing mentions: {e}")

    def _reply_to_mention(self, mention):
        response = random.choice(FUNNY_RESPONSES)
        try:
            reply = self.client.create_tweet(
                text=response,
                in_reply_to_tweet_id=mention.id
            )
            self.logger.info(f"Replied to tweet {mention.id}")
            return reply
        except Exception as e:
            self.logger.error(f"Error replying to mention: {e}")
            return None