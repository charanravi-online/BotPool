import time
from config.settings import MENTION_CHECK_INTERVAL, MAX_RETRIES

class RateLimiter:
    def __init__(self):
        self.retry_count = 0

    def wait(self):
        """Wait for the specified interval"""
        time.sleep(MENTION_CHECK_INTERVAL)
        self.retry_count = 0

    def handle_error(self):
        """Handle rate limit errors with exponential backoff"""
        self.retry_count += 1
        if self.retry_count <= MAX_RETRIES:
            sleep_time = MENTION_CHECK_INTERVAL * (2 ** self.retry_count)
            time.sleep(sleep_time) 