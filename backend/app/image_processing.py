import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO

router = APIRouter()

@router.post("/process-image")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, encoded_image = cv2.imencode('.png', gray_image)
    image_bytes = BytesIO(encoded_image.tobytes())
    
    return StreamingResponse(image_bytes, media_type="image/png")

@router.post("/resize-image")
async def resize_image(file: UploadFile = File(...), width: int = 100, height: int = 100):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    resized_image = cv2.resize(image, (width, height))
    _, encoded_image = cv2.imencode('.png', resized_image)
    image_bytes = BytesIO(encoded_image.tobytes())
    
    return StreamingResponse(image_bytes, media_type="image/png")

@router.post("/rotate-image")
async def rotate_image(file: UploadFile = File(...), angle: int = 90):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, matrix, (w, h))
    _, encoded_image = cv2.imencode('.png', rotated_image)
    image_bytes = BytesIO(encoded_image.tobytes())
    
    return StreamingResponse(image_bytes, media_type="image/png")
