from fastapi import HTTPException
from langchain.chains import LLMChain
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
import aiohttp
from typing import List
import requests
import os
from openai import OpenAI
import logging
from crud import save_image_locally, get_image_filenames

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

def generate_ia_image(text: str):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"pregunta: ¿Cual es tu compromiso de cara al 2030? Esto es para un evento de la empresa McCain. Utiliza esto como contexto. SOLO debes contestar con la imagen puramente visual y obligatoriamente SIN TEXTOS. No puedes generar bebidas alcoholicas. McCain comercializa productos de comida congelada y papas fritas en distintas formas Solo tienes permitido usar la palabra 'McCain'. respuesta: {text}",
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url =response.data[0].url
        image_name = image_url.split("/")[6].split("?")[0]
        logger.info(f"Image name: {image_name}")
        save_image_locally(image_url, image_name)
        return {"image_url": image_url}
    except Exception as e:
        logger.error(f"Error generating IA image: {str(e)}")
        return False
