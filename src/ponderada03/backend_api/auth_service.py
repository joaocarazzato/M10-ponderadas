from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from database.models import User
from database.database import SessionLocal
from fastapi.templating import Jinja2Templates
import uvicorn
from database.models import User
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from typing import Optional



class UserInfo(BaseModel):
    username: str
    password: str

templates = Jinja2Templates(directory="templates")

app = FastAPI()

SECRET_KEY = "pokemon"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

async def get_async_db():
    db = SessionLocal()
    async with db as session:
        yield session

def publish_broker(sensor, message):
    # Configuração do cliente
    client = mqtt.Client("py-publisher")

    # Conecte ao broker
    client.connect("mqtt", 1891, 60)
    # Loop para publicar mensagens continuamente
    try:
        
        message = "" + message
        client.publish(f"{sensor}", message)
        print(f"Publicado: {message} no tópico: '{sensor}'")
    except Exception as e:
        print(f"Finalizando a execução da thread: {e}")

    client.disconnect()

@app.post("/login")
async def login(user_data: UserInfo, db: Session = Depends(get_async_db)):
    async with db as session:
        stmt = select(User).filter(User.name == user_data.username)
        try:
            result = await session.execute(stmt)
            user = result.scalars().one()
            if user and user.password == user_data.password:
                publish_broker("AUTH", f"[AUTH] Usuário com nome de [{user_data.username}] logado com sucesso!")
                return {"status": "Login Success"}
            else:
                publish_broker("AUTH", f"[AUTH] Tentativa de login com usuário: [{user_data.username}] falhou!")
                raise HTTPException(status_code=401, detail="Incorrect username or password")
        except NoResultFound:
            publish_broker("AUTH", f"[AUTH] Tentativa de login com usuário inexistente: [{user_data.username}]!")
            raise HTTPException(status_code=404, detail="User not found")


# Add dependencies to CRUD user endpoints to get current user
@app.get("/users")
async def get_users(db: Session = Depends(get_async_db)):
    async with db as session:

        users = select(User)
        result = await session.execute(users)
        users = result.scalars().all()
    publish_broker("AUTH", f"[USERS] Exibição de todos os usuários requisitada!")
    return users

@app.get("/users/{id}")
async def get_user(id: int, db: Session = Depends(get_async_db)):
    async with db as session:
        stmt = select(User).filter(User.id == id)
        try:
            result = await session.execute(stmt)
            user = result.scalars().one()
            publish_broker("USERS", f"[USERS] Exibição de usuário com o id [{id}] requisitada!")
            return user
        except NoResultFound:
            publish_broker("USERS", f"[USERS] Tentativa de exibição de usuário com o id [{id}] falhou!")
            raise HTTPException(status_code=404, detail="User not found")

@app.post("/users")
async def create_user(user_data: UserInfo, db: Session = Depends(get_async_db)):
    async with db as session:
        db_user = User(name=user_data.username, password=user_data.password)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    publish_broker("AUTH", f"[AUTH] Criação de usuário com o nome de [{user_data.username}] realizada!")
    return {"status": f"User [{user_data.username}] created with id {db_user.id}"}
        
@app.put("/users/{id}")
async def update_user(id: int, user_data: UserInfo, db: Session = Depends(get_async_db)):
    async with db as session:
        db_user = await session.get(User, id)
        if not db_user:
            publish_broker("USERS", f"[USERS] Tentativa de atualização de usuário com o id [{id}] falhou!")
            raise HTTPException(status_code=404, detail="User not found")
        db_user.name = user_data.username
        db_user.password = user_data.password
        await session.commit()

        publish_broker("USERS", f"[USERS] Usuário com o id [{id}] foi atualizado!")
        return {"status": f"User [{user_data.username}] updated"}

@app.delete("/users/{id}")
async def delete_user(id: int, db: Session = Depends(get_async_db)):
    async with db as session:
        db_user = await session.get(User, id)
        if not db_user:
            publish_broker("USERS", f"[USERS] Tentativa de delete de usuário com o id [{id}] falhou!")
            raise HTTPException(status_code=404, detail="User not found")
        await session.delete(db_user)
        await session.commit()
        publish_broker("USERS", f"[USERS] Usuário com o id [{id}] foi deletado!")
        return {"status": f"User with id [{id}] deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
