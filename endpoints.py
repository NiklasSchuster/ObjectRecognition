from fastapi import APIRouter
from starlette import status
from util.pydantic import Image
import base64
from services import ObjectDetector

router = APIRouter()


@router.post("/image", status_code=status.HTTP_201_CREATED, summary="Upload image.")
def image_detector(img: Image):
    
    objects = ObjectDetector.detect_objects(img.image_data)
    
    return {"id": img.id, "objects": objects}