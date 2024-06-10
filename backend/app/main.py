from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base
from app.auth import auth_router
from app.dependencies import get_current_user
from app.image_processing import router as image_processing_router
from app.subscriptions import router as subscriptions_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(image_processing_router, prefix="/image")
app.include_router(subscriptions_router, prefix="/user")

@app.get("/protected-route")
async def protected_route(
    optional_param: str = Query(None)
):
    current_user = Depends(get_current_user)
    return {
        "message": "This is a protected route",
        "user": current_user,
        "optional_param": optional_param
    }
