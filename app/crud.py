import os
import requests
from config import IMAGE_IA_DIR, IMAGE_WORDCLOUD_DIR
from dotenv import load_dotenv
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_text(text: str):
    try:
        logger.info(f"Saving text: {text}")
        text_file = open(f"{IMAGE_WORDCLOUD_DIR}/palabras.txt", "a")
        text_file.write(text + "\n")
        text_file.close()
        return True
    except Exception as e:
        logger.error(f"Error saving text: {str(e)}") 
        return False

def get_all_texts():
    try:
        text_file = open(f"{IMAGE_WORDCLOUD_DIR}/palabras.txt", "r")
        texts = text_file.readlines()
        text_list = [text.strip() for text in texts]
        text_file.close()
        return text_list
    except Exception as e:
        logger.error(f"Error getting all texts: {str(e)}")
        return False

# Guardar la imagen en el directorio local especificado en el archivo .env
def save_image_locally(image_url: str, image_name: str):
    try:
        response = requests.get(image_url)
        image_content = response.content
        save_dir = IMAGE_IA_DIR + image_name
        with open(save_dir, "wb") as file:
            file.write(image_content)
        logger.info(f"Image saved locally at: {save_dir}")
        return save_dir
    except Exception as e:
        logger.error(f"Error saving image locally: {str(e)}")
        return False

def get_image_filenames():
    try:
        # Recuperar nombres de imágenes del directorio local
        image_dir = os.path.dirname(IMAGE_IA_DIR)
        image_filenames = os.listdir(image_dir)
        #add to each image the url to access it
        image_filenames = [f"http://localhost/files/ia/{image}" for image in image_filenames]
        return image_filenames
    except Exception as e:
        logger.error(f"Error getting image filenames: {str(e)}")
        return False

def get_word_cloud_image():
    try:
    # Recuperar nombres de imágenes del directorio local
        image_dir = os.path.dirname(IMAGE_WORDCLOUD_DIR)
        image_filenames = os.listdir(image_dir)
        #add to each image the url to access it
        image_filenames = [f"http://localhost/files/mentimeter/{image}" for image in image_filenames]
        #only return the one with the name wordcloud.png
        image_filenames = [image for image in image_filenames if "wordcloud.png" in image]
        return image_filenames[0]
    except Exception as e:
        logger.error(f"Error getting image filenames: {str(e)}")
        return False