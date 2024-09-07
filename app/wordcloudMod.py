from wordcloud import WordCloud
import os
from crud import get_all_texts
import logging
from config import IMAGE_WORDCLOUD_DIR
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_wordcloud():
    try:
        texts = get_all_texts()
        combined_text = " ".join(texts)
        
        # McCain brand colors
        brand_colors = [
           # '#000000',  # Negro
           # '#434043',  # Gris Oscuro
           '#FFFFFF', #White
           # '#FEDD02',  # Amarillo McCain
           # '#003a72' #azul mccain
           # '#000000',  # Negro
           # '#009863',  # Verde
           # '#C9BFB0',  # Beige
           # '#86CAC6',  # Turquesa
           # '#5D89E9',  # Azul Claro
          #  '#D9DAE4',  # Gris Claro
          #  '#434043',  # Gris Oscuro
          #  '#003B75',  # Azul Oscuro
           # '#EA7603',  # Naranja
           # '#EC3400'   # Rojo
        ]
        
        def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
            return random.choice(brand_colors)

        # Generate word cloud with transparent background
        wordcloud = WordCloud(
            width=1920,
            height=1080,
            background_color=None,  # Set to None for transparent background
            mode='RGBA',  # Use RGBA mode to support transparency
            color_func=random_color_func
        ).generate(combined_text)

        # Save the word cloud image to a file
        image_path = os.path.join(IMAGE_WORDCLOUD_DIR, "wordcloud.png")
        wordcloud.to_file(image_path)

        return True
    except Exception as e:
        logger.error(f"Error generating wordcloud: {str(e)}")
        return False
