from fastapi import FastAPI, UploadFile, File, Response, Form, Depends, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
import uvicorn
import paho.mqtt.client as mqtt
from pydantic import BaseModel
from database.models import Images, User
from sqlalchemy.orm import Session
from database.database import SessionLocal
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc
from sqlalchemy.exc import NoResultFound
import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging





app = FastAPI()

async def get_async_db():
    db = SessionLocal()
    async with db as session:
        yield session

class UserInfo(BaseModel):
    id: int

async def publish_notification(title, body, user_id, db: AsyncSession):
    # Inicialize o SDK do Firebase com suas credenciais
    cred = credentials.Certificate("./serviceKey.json")
    firebase_admin.initialize_app(cred)
    async with db as session:
        stmt = select(User).filter(User.id == int(user_id))
        try:
            result = await session.execute(stmt)
            user = result.scalars().one()
            # Defina a mensagem a ser enviada
            message = messaging.Message(
                notification=messaging.Notification(
                    title=str(title),
                    body=str(body),
                ),
                data={
                    'user_id': str(user_id)
                },
                token= str(user.token_id),
            )
            # Envie a mensagem
            response = messaging.send(message)

            print('Notificação enviada com sucesso:', response)
        except NoResultFound:
            publish_broker("ERROR", f"[USERS] Tentativa de exibição de usuário com o id [{str(user_id)}] falhou!")
            raise HTTPException(status_code=404, detail="User not found")

def publish_broker(sensor, message):
    # Configuração do cliente
    client = mqtt.Client("py-publisher-image")

    # Conecte ao broker
    client.connect("mqtt", 1891, 60)
    # Loop para publicar mensagens continuamente
    try:
        
        message = "" + message
        client.publish(f"service/{sensor}", message)
        print(f"Publicado: {message} no tópico: 'service/{sensor}'")
    except Exception as e:
        print(f"Finalizando a execução da thread: {e}")

    client.disconnect()



async def process_image(contents, user_id, db: AsyncSession):
    print("Processando imagem...")
    await asyncio.sleep(8)
    blob_data = BytesIO(contents)

    async with db as session:
        db_image = Images(content=str(blob_data), user_id=int(user_id))
        session.add(db_image)
        await session.commit()
        await session.refresh(db_image)

        await publish_notification("Sua imagem está pronta!", "Clique aqui para ver sua imagem", str(user_id), db)
        publish_broker("INFO", f"[AUTH] A imagem do usuário de id [{user_id}] foi finalizada!")


async def process_white_image(contents, user_id, db: AsyncSession):
    print("Processando imagem...")
    await asyncio.sleep(8)
    # Abre a imagem a partir dos dados recebidos
    imagem = Image.open(BytesIO(contents))

    # Converte para escala de cinza
    imagem_pb = imagem.convert("L")

    # Salva a imagem em preto e branco em BytesIO
    image_io = BytesIO()
    imagem_pb.save(image_io, format="JPEG")
    image_io.seek(0)

    blob_data = image_io.getvalue()

    async with db as session:
        db_image = Images(content=blob_data, user_id=int(user_id))
        session.add(db_image)
        await session.commit()
        await session.refresh(db_image)

    await publish_notification("Sua imagem está pronta!", "Clique aqui para ver sua imagem", str(user_id), db)
    publish_broker("INFO", f"[AUTH] A imagem do usuário de id [{user_id}] foi finalizada!")
    

@app.post("/upload")
async def upload_image(user_id: str = Form(...) , file: UploadFile = File(...), db: Session = Depends(get_async_db)):
    get_file = await file.read()
    asyncio.create_task(process_image(get_file, user_id, db))

    publish_broker("INFO", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    return {"status": f"Imagem adicionada ao processamento."}

@app.post("/upload_white")
async def upload_image_white(user_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_async_db)):
    get_file = await file.read()
    asyncio.create_task(process_white_image(get_file, user_id, db))

    publish_broker("INFO", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    # Retorna a imagem em preto e branco
    return {"status": f"Imagem adicionada ao processamento."}

@app.post("/get_image")
async def get_image(user_data: UserInfo, db: Session = Depends(get_async_db)):
    async with db as session:
        stmt = select(Images).filter(Images.user_id == user_data.id).order_by(desc(Images.id)).limit(1)
        try:
            result = await session.execute(stmt)
            image = result.scalars().one()
            print(image.content)
            image_to_send = BytesIO(image.content)
            image_to_send.seek(0)
            return StreamingResponse(image_to_send, media_type='image/jpeg')
        except NoResultFound:
            publish_broker("ERROR", f"[AUTH] Tentativa de recebimento de imagem com imagem inexistente do id: [{user_data.id}]!")
            raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)