# Aplicação Flutter To-do List com conexão API assíncrona em FastAPI

A ideia desse repositório é a criação de uma API de uma aplicação To-do List feita em FastAPI utilizando uma interface feita para mobile em Flutter.

A documentação da API pode ser encontrada dentro da pasta **docs**, tanto com um export das Collections do **Insomnia** para testar a api, quanto sua documentação **Swagger**.

[Screencast from 10-05-2024 10:24:40.webm](https://github.com/joaocarazzato/M10-ponderadas/assets/99187756/0d2a0170-8bbd-4138-bd09-797430d2e8f5)

## Como executar?
Para executar, primeiro precisamos baixar a source da aplicação e rodar nosso container docker dentro da pasta **backend_api** com o seguinte comando:
```
docker compose up
```

Após isso, teremos nosso backend rodando em um container docker, então só temos que iniciar nossa aplicação para termos uma API com interface funcionando:
```
flutter run
```

Com isso, só precisamos acessar o aplicativo através de seu emulador do Android Studio ou seu próprio aparelho.

Com isso, podemos usar toda a interface da aplicação e as rotas documentadas tanto pelo Insomnia, quanto Swagger, quanto interface, sendo possível fazer um CRUD completo.
