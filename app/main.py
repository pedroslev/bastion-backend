import sys
import os
from pathlib import Path
import logging
from dotenv import load_dotenv

# Add the parent directory of 'app' to the Python path
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(str(Path(__file__).parent))


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server_port = int(os.getenv("PORT", 8000))

app = FastAPI(
    title="bastion-service",
    version="1.0",
    description="Interface for Bastion McCain's AI services",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the chain routes
app.include_router(router, prefix="/api/v1")

@app.get("/status")
async def root():
    return {"message": f"bastion-service is running on version {app.version}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=server_port)