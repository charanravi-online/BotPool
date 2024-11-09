import os
import random
from config.settings import MEDIA_FOLDER
from src.utils.logger import setup_logger

class MediaHandler:
    def __init__(self, api):
        self.api = api
        self.logger = setup_logger()
        self.meme_folder = os.path.join(MEDIA_FOLDER, 'memes')
        self.gif_folder = os.path.join(MEDIA_FOLDER, 'gifs')

    def get_random_media(self):
        """Get a random media file from the media folders"""
        try:
            media_files = (
                [f for f in os.listdir(self.meme_folder) if f.endswith(('.jpg', '.png', '.gif'))] +
                [f for f in os.listdir(self.gif_folder) if f.endswith('.gif')]
            )
            if media_files:
                return os.path.join(MEDIA_FOLDER, random.choice(media_files))
        except Exception as e:
            self.logger.error(f"Error getting random media: {e}")
        return None 