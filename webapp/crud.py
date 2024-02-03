from sqlalchemy.orm import Session
import models, schemas

# def 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
                        username=user.username, 
                        first_name=user.first_name, 
                        last_name=user.last_name, 
                        hashed_password=fake_hashed_password
                    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
