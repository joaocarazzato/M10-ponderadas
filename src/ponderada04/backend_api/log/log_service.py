import paho.mqtt.client as mqtt
from fastapi import FastAPI
import threading
import uvicorn
from models.logging_config import LoggerSetup
import logging

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)


app = FastAPI()
banco_em_memoria = []


# Callback quando uma mensagem é recebida do servidor.
def on_message(client, userdata, message):
    topic = message.topic.upper()
    received_message = message.payload.decode()
    print(f"Recebido: {received_message} no tópico {topic}")

    if topic == "SERVICE/INFO":
        LOGGER.info({"message": received_message})
    elif topic == "SERVICE/WARN":
        LOGGER.warning({"message": received_message})
    elif topic == "SERVICE/ERROR":
        LOGGER.error({"message": received_message})
    elif topic == "SERVICE/CRITICAL":
        LOGGER.critical({"message": received_message})
    else:
        pass
    banco_em_memoria.append(received_message)

# Callback para quando o cliente recebe uma resposta CONNACK do servidor.
def on_connect(client, userdata, flags, rc):
    print("Conectado ao broker com código de resultado "+str(rc))
    # Inscreva no tópico aqui, ou se perder a conexão e se reconectar, então as
    # subscrições serão renovadas.
    client.subscribe("service/#")

@app.get("/messages")
async def get_messages():
    return banco_em_memoria

    # Configuração do cliente
def run_mqtt():
    client = mqtt.Client("python_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

    # Conecte ao broker
    client.connect("mqtt", 1891, 60)

    # Loop para manter o cliente executando e escutando por mensagens
    client.loop_forever()

if __name__ == "__main__":
    try:
        thread = threading.Thread(target=run_mqtt)
        thread.start()
        uvicorn.run(app, host="0.0.0.0", port=5100)
    except Exception as e:
        print(f"Finalizando a execução da thread: {e}")
        thread.stop()