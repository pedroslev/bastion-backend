from wordcloud import WordCloud
import os
from crud import get_all_texts
import logging
from config import  IMAGE_WORDCLOUD_DIR

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_wordcloud():
    try:
        texts = get_all_texts()
        combined_text = " ".join(texts)
        wordcloud = WordCloud(width=800, height=400).generate(combined_text)
        image_path = f"{IMAGE_WORDCLOUD_DIR}/wordcloud.png"
        wordcloud.to_file(image_path)
        return image_path
    except Exception as e:
        logger.error(f"Error generating wordcloud: {str(e)}")
        return False

