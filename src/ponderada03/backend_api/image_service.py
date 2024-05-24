from fastapi import FastAPI, UploadFile, File, Response, Form
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
import uvicorn
import paho.mqtt.client as mqtt
from pydantic import BaseModel


app = FastAPI()

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

@app.post("/upload")
async def upload_image(user_id: str = Form(...) , file: UploadFile = File(...)):
    print(user_id)
    contents = await file.read()
    publish_broker("IMAGE", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    return Response(contents, media_type="image/jpeg")

@app.post("/upload_white")
async def upload_image(user_id: str = Form(...), file: UploadFile = File(...)):
    print(user_id)
    # Lê o conteúdo da imagem
    contents = await file.read()

    # Abre a imagem a partir dos dados recebidos
    imagem = Image.open(BytesIO(contents))

    # Converte para escala de cinza
    imagem_pb = imagem.convert("L")

    # Salva a imagem em preto e branco em BytesIO
    image_io = BytesIO()
    imagem_pb.save(image_io, format="JPEG")
    image_io.seek(0)

    publish_broker("IMAGE", f"[IMAGE] Recebido imagem para processar do usuário de id [{user_id}]")
    # Retorna a imagem em preto e branco
    return StreamingResponse(image_io, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)