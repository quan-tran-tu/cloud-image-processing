from sqlalchemy.orm import Session
from .models import User, Subscription
from .schemas import UserCreate, SubscriptionCreate
from .utils import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_subscription(db: Session, subscription: SubscriptionCreate, user_id: int):
    db_subscription = Subscription(**subscription.dict(), user_id=user_id)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_subscriptions_by_user(db: Session, user_id: int):
    return db.query(Subscription).filter(Subscription.user_id == user_id).all()
