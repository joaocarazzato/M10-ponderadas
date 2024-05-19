from fastapi import FastAPI, UploadFile, File, Response
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    return Response(contents, media_type="image/jpeg")

@app.post("/upload_white")
async def upload_image(file: UploadFile = File(...)):
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

    # Retorna a imagem em preto e branco
    return StreamingResponse(image_io, media_type="image/jpeg")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5200)