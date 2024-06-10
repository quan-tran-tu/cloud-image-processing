from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import SubscriptionCreate, Subscription
from .crud import create_subscription, get_subscriptions_by_user
from .dependencies import get_current_user, oauth2_scheme

router = APIRouter()

@router.post("/subscriptions", response_model=Subscription)
def create_user_subscription(
    subscription: SubscriptionCreate,
    token: str = Depends(oauth2_scheme)
):
    db = SessionLocal()
    current_user = get_current_user(token, db)
    return create_subscription(db, subscription, user_id=current_user.id)

@router.get("/subscriptions", response_model=list[Subscription])
def read_user_subscriptions(
    token: str = Depends(oauth2_scheme)
):
    db = SessionLocal()
    current_user = get_current_user(token, db)
    subscriptions = get_subscriptions_by_user(db, user_id=current_user.id)
    if subscriptions is None:
        raise HTTPException(status_code=404, detail="Subscriptions not found")
    return subscriptions
