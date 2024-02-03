# Desafio

Usando [Django](https://www.djangoproject.com/) e [Django REST framework](https://www.django-rest-framework.org/) desenvolva uma API REST que permita usuários gerenciar empréstimos.

## Crtérios de aceite
* Usuários devem ser capazes de inserir empréstimos e seus respectivos pagamentos
* Usuários devem ser capazer de visualizar seus empréstimos e pagamentos
* Usuários devem ser capazes de visualizar o [saldo devedor](https://duckduckgo.com/?q=saldo+devedor) de cada um dos seus empréstimos
    * Você pode decidir onde e como mostrar a informação
    * O saldo devedor nada mais é do que o quanto o cliente ainda deve para o banco
    * O saldo devedor deve considerar a taxa de juros do empréstimo e descontar o que já foi pago
* Usuários não podem ver ou editar empréstimos ou pagamentos de outros usuários
* A autenticação da API deve ser feita via token
    * Não é necessário desenvolver endpoints para criação/gerenciamento de usuários
* Os empréstimos devem conter no mínimo as informações abaixo:
    * Identificador - um identificador aleatório gerado automaticamente
    * Valor nominal - o valor emprestado pelo banco
    * Taxa de juros - a taxa de juros mensal do empréstimo
    * Endereço de IP - endereço de IP que cadastrou o empréstimo
    * Data de solicitação - a data em que o empréstimo foi solicitado
    * Banco - informações do banco que emprestou o dinheiro (pode ser um simples campo de texto)
    * Cliente - informações do cliente que pegou o empréstimo (pode ser um simples campo de texto)
* Os pagamentos devem conter no mínimo as informações abaixo:
    * Identificador do empréstimo
    * Data do pagamento
    * Valor do pagamento
* Testes
    * As funcionalidade principais devem estar com [testes](https://docs.djangoproject.com/en/3.1/topics/testing/) escritos
    * Você pode decidir quais os testes que mais agregam valor ao projeto

## Setup

### Pre-requisitos

- Docker
- Python

### Para rodar o projeto
Na raiz do projeto, execute as seguintes ações

- Crie o ambiente virtual:
  `python3 -m venv .venv`

- Ative o ambiente virtual:
` source .venv/bin/activate`

- Instale as dependências do projeto:
  `pip install -r requirements.txt`

- Construa a imagem docker que cria o banco de dados:
  `docker build -t matera-db .`

- Rode o container:
  `docker run -d -p 3306:3306 --name=matera-mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=matera_database matera-db`

- Rode as migrações:
  `python3 manage.py migrate`

- Crie um superuser se necessário:
  `python3 manage.py createsuperuser`

- Rode o servidor Django:
  `python3 manage.py runserver`

### Para testar

- Para rodar os testes automatizados que foram implementados:
`python3 -m pytest`

- Para verificar erros de estilo:
`python3 -m flake8`

## Documentação

- Para ver a documentação das rotas da API, acesse http://127.0.0.1:8000/swagger/
