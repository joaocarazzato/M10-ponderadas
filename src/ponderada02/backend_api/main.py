from fastapi import Form, Depends, Request, HTTPException, Response, FastAPI, Body
from sqlalchemy.orm import Session
from database.models import ToDoList
from database.database import SessionLocal, db, engine
from fastapi.templating import Jinja2Templates
import uvicorn

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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
