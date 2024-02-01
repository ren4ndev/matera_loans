### Setup

#### Pre-requisitos

- Docker
- Python

#### Para rodar

- `python3 -m venv .venv`

- `source .venv/bin/activate`

- `pip install -r requirements.txt`

- `docker build -t matera-db .`

- `docker run -d -p 3306:3306 --name=matera-mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=matera_database matera-db`

- `python3 manage.py migrate`

- `python3 manage.py createsuperuser`

- `python3 manage.py runserver`
