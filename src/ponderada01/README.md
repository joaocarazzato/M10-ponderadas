# API To-Do List com proteção de rotas
A ideia desse repositório é a criação de uma API de uma aplicação To-do List feita em Flask utilizando uma proteção de rotas feita com JWT.

A documentação da API pode ser encontrada dentro da pasta **docs**, tanto com um export das Collections do **Insomnia** para testar a api, quanto sua documentação **Swagger**.

## Como executar?
Para executar, primeiro precisamos baixar as bibliotecas Flask, flask_jwt_extended e Flask_sqlalchemy, após isso precisamos digitar o seguinte comando para criar um banco de dados para nós:
```
python3 main.py create_db
```

Após isso, teremos uma pasta chamada Instance com um banco em sqlite3, então só temos que iniciar nossa aplicação para termos uma API com interface funcionando:
```
python3 -m flask --app main run
```

Com isso, só precisamos acessar o seguinte endereço: [http://localhost:5000/user-login](http://localhost:5000/user-login)

Com isso, podemos usar toda a interface da aplicação e as rotas documentadas tanto pelo Insomnia, quanto Swagger, quanto interface.
