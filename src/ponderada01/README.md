# API To-Do List síncrona e assíncrona
A ideia desse repositório é a criação de uma API de uma aplicação To-do List feita tanto de forma síncrona usando Flask quanto assíncrona utilizando FastAPI, afim de fazer uma série de testes para comparar seus resultados.

A documentação da API pode ser encontrada dentro da pasta **docs**, tanto com um export das Collections do **Insomnia** para testar a api, quanto sua documentação **Swagger**. Além disso, podemos encontrar o teste de carga realizado utilizando o JMeter na pasta raiz, o teste se trata de requisições GET a fim de ver como a aplicação se comportava com uma requisição mais simples.

A partir disso, entendemos que nesse caso a API síncrona teve uma performance melhor. Apesar de ter tido requisições mais consistentes em questão do tempo de resposta, houve um maior consumo de dados em Kilobytes do que a versão assíncrona, que acabou perdendo em tempo de resposta por poucos milissegundos. Outro fator interessante foi como ambas se comportaram com um grande número de requisições, apesar de terem lidado bem com um número elevado de 100 requisições, tiveram problemas para lidar com quantidades maiores - visto que houve uma limitação por parte do banco devido a forma como as rotas foram criadas(sem um sistema de cache do banco), sobrecarregando ambas aplicações.

## Como executar?
Para executar, primeiro precisamos baixar o repositório, e então, após entrar na pasta do estilo da aplicação que deseja, precisamos digitar o seguinte comando para criar os containers dockerizados para nós:
```
docker compose up
```

Após isso, teremos uma aplicação containerizada com um banco de dados em PostgreSQL. Caso queiramos parar a nossa aplicação, é só utilizar o atalho **Cntrl + C** e então digitar o seguinte comando:
```
docker compose down
```

Apesar de recomendarmos os testes de funcionalidade via os **Collections do Insomnia**, podemos acessar o seguinte endereço para verificar sua funcionalidade: [http://localhost:5000/](http://localhost:5000/)

Com isso, podemos usar a API da aplicação com as rotas documentadas tanto pelo Insomnia, quanto Swagger, quanto interface.

(Mudanças podem ser feitas no banco de dados e tabelas a serem criados editando o arquivo **db.sql**, porém necessitando de mudanças também em todo o resto da aplicação para poder ser usada).
