# Endpoint 1: Generar imagen con DALL-E
from fastapi import APIRouter, Body
from pydantic import BaseModel
import time
from crud import get_image_filenames, save_text, get_word_cloud_image, insert_text_to_excel, insert_text_to_excel_momento, get_momento, create_ia_mosaic, insert_momento4_to_excel, insert_training_to_excel, insert_ia_to_excel, get_momento2
from app.wordcloudMod import generate_wordcloud
from ia import generate_ia_image, random_selector, generate_ia_image_lowQ
import logging
import random
from config import IMAGE_WORDCLOUD_DIR, STATE_DIR, SERVE_IMAGE, IMAGE_IA_DIR

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class textModel(BaseModel):
    text: str

class imageGeneratorModel(BaseModel):
    name: str
    text: str

class momentoModel(BaseModel):
    pregunta1: str
    pregunta2: str
    pregunta3: str

class momento4Model(BaseModel):
    content: int
    duration: int
    food: int
    location: int
    presentation1: int
    question1: str
    question2: str
    speaker1: int
    speaker2: int
    summit: int



class trainingModel(BaseModel):
    AwardsEvent: int
    TrainingWednesday: int
    TrainingThursday: int
    question1: str
    question2: str
    


#generate IA image
@router.post("/generate")
def generate_image(request: imageGeneratorModel = Body(...)):
    logger.info(f"New request for image generation: {request.text} from {request.name}")
    text_file = open(STATE_DIR, "r")
    texts = text_file.readlines()
    text_list = [text.strip() for text in texts]
    text_file.close()
    state =  text_list[0]
    if state == "IA":
        try:
            image_url = generate_ia_image(request.text)
            image_name = image_url['image_url'].split("/")[-1]
            insert_ia_to_excel("ia.xlsx", request.text, request.name, image_name)
            return image_url
        except Exception as e:
            try:
                image_url = generate_ia_image_lowQ(request.text)
                image_name = image_url['image_url'].split("/")[-1]
                insert_ia_to_excel("ia.xlsx", request.text, request.name, image_name)
                return image_url
            except Exception as e:        
                logger.error("Error generating IA image, defaulting")
                image_selected = random_selector()
                insert_ia_to_excel("ia.xlsx", request.text, request.name, image_selected)
                response = {"image_url": f"{SERVE_IMAGE}/files/ia/{image_selected}"}
                #wait randomly between 5 and 15 seconds before returning response
                time.sleep(random.randint(5, 15))
                return response
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
async def moment1(request: momentoModel = Body(...)):
    try:
        logger.info(f"New request for form momento 1 insertion: {request}")
        insert_text_to_excel_momento("latamTopInitiatives.xlsx", request)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.get("/moment1")
async def moment1get():
    try:
        logger.info(f"New request for getting momento 1 answers")
        respuestas = get_momento()
        return {"status": "Text saved successfully", "code": 200, "respuestas": respuestas}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.post("/moment2")
async def moment2(request: textModel = Body(...)):
    try:
        logger.info(f"New request for form momento 2 insertion: {request}")
        insert_text_to_excel("biggestTakeaway.xlsx", request.text)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error getting moment1: {str(e)}", "code": 500}

@router.get("/moment2")
async def moment2get():
    try:
        logger.info(f"New request for getting momento 1 answers")
        respuestas = get_momento2()
        return {"status": "Text saved successfully", "code": 200, "respuestas": respuestas}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.post("/moment3")
async def moment3(request: textModel = Body(...)):
    try:
        logger.info(f"New request for form momento 3 insertion: {request}")
        insert_text_to_excel("highlights.xlsx", request.text)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}

@router.post("/moment4")
async def moment4(request: momento4Model = Body(...)):
    try:
        logger.info(f"New request for form momento4 insertion: {request}")
        insert_momento4_to_excel("summitFeedback.xlsx", request)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}
    
@router.post("/training")
async def training(request: trainingModel = Body(...)):
    try:
        logger.info(f"New request for training response insertion: {request}")
        insert_training_to_excel("training.xlsx", request)
        return {"status": "Text saved successfully", "code": 200}
    except Exception as e:
        return {"status": f"Error saving moment1: {str(e)}", "code": 500}
    
