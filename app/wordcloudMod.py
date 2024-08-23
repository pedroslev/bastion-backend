from wordcloud import WordCloud
import os
from crud import get_all_texts
import logging
from config import  IMAGE_WORDCLOUD_DIR
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_wordcloud():
    try:
        texts = get_all_texts()
        combined_text = " ".join(texts)
        #mccain colors
        brand_colors = [
            '#fee000',  # Amarillo McCain
            '#000000',  # Negro
            '#009863',  # Verde
            '#C9BFB0',  # Beige
            '#86CAC6',  # Turquesa
            '#5D89E9',  # Azul Claro
            '#D9DAE4',  # Gris Claro
            '#434043',  # Gris Oscuro
            '#003B75',  # Azul Oscuro
            '#EA7603',  # Naranja
            '#EC3400'   # Rojo
        ]
        def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
            return random.choice(brand_colors)
        
        wordcloud = WordCloud(
            width=11811,
            height=4724,
            background_color='#ffff',
            color_func=random_color_func).generate(combined_text)
        image_path = f"{IMAGE_WORDCLOUD_DIR}/wordcloud.png"
        wordcloud.to_file(image_path)
        return True
    except Exception as e:
        logger.error(f"Error generating wordcloud: {str(e)}")
        return False

