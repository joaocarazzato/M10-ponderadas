from fastapi import Form, Depends, Request, HTTPException, Response, FastAPI, Body
from sqlalchemy.orm import Session
from database.models import User, ToDoList
from database.database import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import uvicorn
from database.database import db, engine
from database.models import User, ToDoList

templates = Jinja2Templates(directory="templates")

app = FastAPI()

SECRET_KEY = "pokemon"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

db.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.name == username).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = db.query(User).filter(User.name == username).first()
    if user is None:
        raise credentials_exception
    return user

# Update /token endpoint to use OAuth2PasswordRequestForm
@app.post("/token")
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}

# Update /login endpoint to use OAuth2PasswordRequestForm
@app.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)
    all_posts = await get_all_posts()
    return templates.TemplateResponse("content.html", {"request": Request, "all_posts": all_posts})

# Add dependencies to CRUD endpoints to get current user
@app.get("/posts")
async def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(ToDoList).all()
    return posts

@app.get("/posts/{id}")
async def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(ToDoList).filter(ToDoList.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{id}")
async def update_post_by_id(id: int, post_name: str = Body(...), post_content: str = Body(...), db: Session = Depends(get_db)):
    db_post = db.query(ToDoList).filter(ToDoList.id == id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    db_post.post_name = post_name
    db_post.post_content = post_content
    db.commit()
    return db_post

@app.delete("/posts/{id}")
async def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(ToDoList).filter(ToDoList.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return post

@app.post("/posts")
async def create_post(post_name: str = Body(...), post_content: str = Body(...), db: Session = Depends(get_db)):
    db_post = ToDoList(post_name=post_name, post_content=post_content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Add dependencies to CRUD user endpoints to get current user
@app.get("/users")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def create_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = User(name=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{id}")
async def update_user(id: int, username: str, password: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = username
    db_user.password = password
    db.commit()
    return db_user

@app.delete("/users/{id}")
async def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
