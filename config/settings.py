from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Twitter API credentials
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Verify all credentials are loaded
required_vars = [
    'TWITTER_BEARER_TOKEN',
    'TWITTER_API_KEY',
    'TWITTER_API_SECRET',
    'TWITTER_ACCESS_TOKEN',
    'TWITTER_ACCESS_TOKEN_SECRET'
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Bot Settings
TWEET_INTERVAL = 14400  # 4 hours in seconds
MENTION_CHECK_INTERVAL = 900  # 15 minutes in seconds
MAX_RETRIES = 3
MEDIA_FOLDER = 'data/media'

# Logging
LOG_FILE = 'twitter_bot.log'
LOG_LEVEL = 'INFO' 