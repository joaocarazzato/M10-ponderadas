# Sistema de aplicação de filtros em fotos com sistema de autenticação, fila, notificações e log
O objetivo desse repositório é a entrega da ponderada onde o objetivo era a criação de um sistema completo em microsserviços com sistema de logging.

[Screencast from 25-05-2024 04:18:16.webm](https://github.com/joaocarazzato/M10-ponderadas/assets/99187756/5005a254-79f6-4d1e-aee7-d1ca13b0b627)

## O que o sistema possui?

- Backend em microsserviços
  - Autenticação: É possível criar contas e logar no serviço, para que seja possível registrar imagens no seu usuário a fim de receber notificações quando elas ficarem prontas.
  - Manipulação de imagem: É possível enviarmos imagens para uma fila a fim de processá-la e aplicar filtros na mesma, recebendo uma notificação e obtendo-a quando ela ficar pronta.
  - Notificações: Notificações são enviadas assim que a imagem termina seu processamento, afim do usuário poder visualizá-la com mais facilidade com essa informação.
  - Logging: Possuímos um sistema de logs, tanto pelo endpoint quanto pelos arquivos, registrando falhas, falhas críticas e avisos que podem ajudar a depurar bugs, erros e outros casos.
  - Gateway NGINX: Responsável por juntar todos esses sistemas em um lugar só, sendo o intermediário entre o usuário e o backend.

## Como executar?

Primeiro, para executar a aplicação, é necessário abrir seu emulador ou seu celular android e digitar o seguinte comando na parte de **mobile**:

```
flutter run
```

Após isso, ao carregar a aplicação, precisamos rodar nosso backend para que a aplicação funcione e seja possível utilizá-la. Ao entrar na pasta de **backend**, digite o seguinte comando:

```
docker compose up --build
```

Assim, será possível utilizar a aplicação igual ao vídeo e visualizar os logs em uma pasta chamada **logs_volume** que será criada.
