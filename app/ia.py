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
            prompt = f"""
Crea una imagen corporativa que represente visualmente el compromiso personal expresado en la palabra (no más de 2) '{text}', incorporando los colores principales de McCain Foods (amarillo, naranja, negro y blanco) y destacando los elementos clave de los pilares estratégicos de McCain Foods para 2030: Liderazgo indiscutible en Papa, Mas del Menú y de Bueno a Excepcional.
Instrucciones adicionales para el modelo AI:
Personalización: Cada imagen debe ser única y reflejar la esencia del compromiso individual, conectando visualmente con los pilares de la estrategia al 2030.
Colores Corporativos: El uso predominante de los colores de McCain Foods debe ser respetado, asegurando la coherencia visual con la identidad de la marca.
Estilo Corporativo: Las imágenes deben mantener un estilo profesional y alineado con la identidad visual de McCain Foods, con un enfoque en la claridad y el impacto visual.
Prohibido Usar: bebidas alcohólicas, imágenes infantiles o con niños, imágenes que sean ofensivas.
""",
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
