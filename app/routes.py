# Endpoint 1: Generar imagen con DALL-E
from fastapi import APIRouter, Body
from pydantic import BaseModel
import sys
from crud import get_image_filenames, save_text, get_word_cloud_image, insert_text_to_excel, insert_text_to_excel_momento, get_momento, create_ia_mosaic
from app.wordcloudMod import generate_wordcloud
from ia import generate_ia_image
import logging
from config import IMAGE_WORDCLOUD_DIR, STATE_DIR, SERVE_IMAGE

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class textModel(BaseModel):
    text: str

class momentoModel(BaseModel):
    pregunta1: str
    pregunta2: str
    pregunta3: str

#generate IA image
@router.post("/generate")
def generate_image(request: textModel = Body(...)):
    logger.info(f"New request for image generation: {request.text}")
    text_file = open(STATE_DIR, "r")
    texts = text_file.readlines()
    text_list = [text.strip() for text in texts]
    text_file.close()
    state =  text_list[0]
    if state == "IA":
        image_url = generate_ia_image(request.text)
        return image_url
    else:
        return {"status": "Conflic generating image", "code": 409, "msg": "The state is not IA"}

#Get IA images urls.
@router.get("/images")
async def list_images():
    images = get_image_filenames()
    return images

#Mosaic for IA
@router.get("/mosaic")
async def mosaic():
    try:
        creation = create_ia_mosaic()
        if creation:
            image_url = f"{SERVE_IMAGE}/files/mosaic/mosaic.png"
            return {"image_url": image_url, "status": "Mosaic created successfully", "code": 200}
        else:
            return {"status": "Error creating mosaic", "code": 500}
    except FileNotFoundError:
        return {"status": "File not found", "code": 404}
    except Exception as e:
        return {"status": f"Error getting mosaic: {str(e)}", "code": 500}


#get the wordcloud image url.
@router.get("/wordcloud")
async def get_wordcloud():
    try:
        image = get_word_cloud_image()
        return image
    except FileNotFoundError:
        return {"status": "File not found", "code": 404}
    except Exception as e:
        return {"status": f"Error getting wordcloud image: {str(e)}", "code": 500}

#save text to generate wordcloud later
@router.post("/push-text")
async def push_text(request: textModel = Body(...)):
    save_text(request.text)
    return {"status": "Text saved successfully", "code": 200}

#Generate wordcloud image
@router.get("/generate-wordcloud")
async def wordcloud():
    try:
        generation = generate_wordcloud()
        if generation:
            image_url = f"{SERVE_IMAGE}/files/wordcloud/wordcloud.png"
        return {"wordcloud_image_url": image_url}
    except:
        logger.error("Error generating wordcloud")
        return {"status": "Error generating wordcloud", "code": 500}

#Restart wordcloud texts
@router.get("/restart-wordcloud")
async def restart_wordcloud():
    try:
        with open(f"{IMAGE_WORDCLOUD_DIR}/palabras.txt", "w") as file:
            file.write("")
        return {"status": "Wordcloud restarted successfully", "code": 200}
    except FileNotFoundError:
        return {"status": "File not found", "code": 404}
    except Exception as e:
        return {"status": f"Error restarting wordcloud: {str(e)}", "code": 500}
    
#get state
@router.get("/load")
async def load():
    try:
        text_file = open(STATE_DIR, "r")
        texts = text_file.readlines()
        text_list = [text.strip() for text in texts]
        text_file.close()
        return text_list[0]
    except FileNotFoundError:
        return {"status": "File not found", "code": 404}
    except Exception as e:
        return {"status": f"Error getting state: {str(e)}", "code": 500}
    
@router.post("/state")
async def save_state(request: textModel = Body(...)):
    try:
        with open(STATE_DIR, "w") as file:
            file.write(request.text)
        return {"status": "State saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving state: {str(e)}", "code": 500}
    
@router.post("/moment1")
async def momentOne(request: momentoModel = Body(...)):
    try:
        insert_text_to_excel_momento("momento1.xlsx", request)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.get("/moment1")
async def momentOne():
    try:
        respuestas = get_momento()
        return {"status": "Text saved successfully", "code": 200, "respuestas": respuestas}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.post("/moment2")
async def momentOne(request: textModel = Body(...)):
    try:
        insert_text_to_excel("momento2.xlsx", request.text)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error getting moment1: {str(e)}", "code": 500}

@router.post("/moment3")
async def momentOne(request: textModel = Body(...)):
    try:
        insert_text_to_excel("momento3.xlsx", request.text)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.post("/moment4")
async def momentOne(request: textModel = Body(...)):
    try:
        insert_text_to_excel("momento4.xlsx", request.text)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}