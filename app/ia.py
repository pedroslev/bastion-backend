from fastapi import HTTPException
import time
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
import aiohttp
from typing import List
import random
import json
import requests
import os
from openai import OpenAI
import logging
from config import SERVE_IMAGE, IMAGE_IA_DIR
from crud import save_image_locally, get_image_filenames
from collections import deque


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

# Rate limit parameters
REQUESTS_PER_MINUTE = 5
SECONDS_BETWEEN_REQUESTS = 60 / REQUESTS_PER_MINUTE
request_queue = deque()  # Queue to manage multiple requests

# Function to generate IA image with rate limiting
def generate_ia_image(text: str):
    # Add the request to the queue
    request_queue.append(text)

    # Process the queue while respecting the rate limit
    while request_queue:
        try:
            # Retrieve the next text from the queue
            text = request_queue.popleft()

            # OpenAI API request
            response = client.images.generate(
                model="dall-e-3",
                prompt = f"""
Crea una imagen corporativa para McCain que represente visualmente el compromiso expresado en '{text}' a la pregunta "what is your commitment for 2030, usando amarillo, naranja, negro y blanco como colores principales
Personalización: Cada imagen debe ser única y reflejar la esencia del compromiso individual, conectando visualmente con los pilares.
Estilo: estilo profesional con un enfoque en la claridad y el impacto visual.
Prohibido Usar: bebidas alcohólicas o imágenes que sean ofensivas.
""",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # Process response
            image_url = response.data[0].url
            image_name = image_url.split("/")[6].split("?")[0]
            logger.info(f"Image name: {image_name}")

            # Save the image and generate the serving URL
            save_dir = save_image_locally(image_url, image_name)
            image_serve_url = save_dir.replace("/app", SERVE_IMAGE)
            logger.info(f"Image saved at {image_serve_url}")

            # Return the generated image URL
            return {"image_url": image_serve_url}

        except Exception as e:
            logger.error(f"Error generating IA image: {str(e)}")
            return False

def generate_ia_image_lowQ(text: str):
    # Add the request to the queue
    request_queue.append(text)

    # Process the queue while respecting the rate limit
    while request_queue:
        try:
            # Retrieve the next text from the queue
            text = request_queue.popleft()

            # OpenAI API request
            response = client.images.generate(
                model="dall-e-2",
                prompt = f"""
Crea una imagen corporativa para McCain que represente visualmente el compromiso expresado en '{text}' a la pregunta "what is your commitment for 2030, usando amarillo, naranja, negro y blanco como colores principales
Personalización: Cada imagen debe ser única y reflejar la esencia del compromiso individual, conectando visualmente con los pilares.
Estilo: estilo profesional con un enfoque en la claridad y el impacto visual.
Prohibido Usar: bebidas alcohólicas o imágenes que sean ofensivas.
""",
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # Process response
            image_url = response.data[0].url
            image_name = image_url.split("/")[6].split("?")[0]
            logger.info(f"Image name: {image_name}")

            # Save the image and generate the serving URL
            save_dir = save_image_locally(image_url, image_name)
            image_serve_url = save_dir.replace("/app", SERVE_IMAGE)
            logger.info(f"Image saved at {image_serve_url}")

            # Return the generated image URL
            return {"image_url": image_serve_url}

        except Exception as e:
            logger.error(f"Error generating IA image: {str(e)}")
            return False



def random_selector():
    images = [f for f in os.listdir(IMAGE_IA_DIR) if os.path.isfile(os.path.join(IMAGE_IA_DIR, f)) and f.lower().endswith('.png')]
    record_file = "selected_files.json"
    # Load the record of selected files
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            try:
                selected_files = json.load(f)
            except json.JSONDecodeError:
                selected_files = []
    else:
        selected_files = []
    
    # Identify files that have not yet been selected
    remaining_files = list(set(images) - set(selected_files))
    
    if not remaining_files:
        # All files have been selected; reset the record
        selected_files = []
        remaining_files = images.copy()
    
    # Randomly select a file from the remaining files
    selected_file = random.choice(remaining_files)
    
    # Update the record of selected files
    selected_files.append(selected_file)
    with open(record_file, 'w') as f:
        json.dump(selected_files, f)
    
    # Return the full path to the selected file
    return selected_file