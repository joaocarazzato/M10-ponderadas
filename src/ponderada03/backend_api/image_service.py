from fastapi import FastAPI, UploadFile, File, Response, Form, Depends
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
import uvicorn
import paho.mqtt.client as mqtt
from pydantic import BaseModel
from database.models import Images
from sqlalchemy.orm import Session
from database.database import SessionLocal
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession




app = FastAPI()

async def get_async_db():
    db = SessionLocal()
    async with db as session:
        yield session

class UserInfo(BaseModel):
    id: int

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

        publish_broker("AUTH", f"[AUTH] A imagem do usuário de id [{user_id}] foi finalizada!")


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
        db_image = Images(content=str(blob_data), user_id=int(user_id))
        session.add(db_image)
        await session.commit()
        await session.refresh(db_image)
        publish_broker("AUTH", f"[AUTH] A imagem do usuário de id [{user_id}] foi finalizada!")
    

@app.post("/upload")
async def upload_image(user_id: str = Form(...) , file: UploadFile = File(...), db: Session = Depends(get_async_db)):
    get_file = await file.read()
    asyncio.create_task(process_image(get_file, user_id, db))

    publish_broker("IMAGE", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    return {"status": f"Imagem adicionada ao processamento."}

@app.post("/upload_white")
async def upload_image_white(user_id: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_async_db)):
    get_file = await file.read()
    asyncio.create_task(process_white_image(get_file, user_id, db))

    publish_broker("IMAGE", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    # Retorna a imagem em preto e branco
    return {"status": f"Imagem adicionada ao processamento."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)