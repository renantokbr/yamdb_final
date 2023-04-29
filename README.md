
![Yamdb Workflow Status](https://github.com/renantokbr/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

Стек:
- Django 4.1.1
- DRF 3.14.0
- djangorestframework-simplejwt 5.2.1
- psycopg2-binary 2.9.3
- PyJWT 2.5.0

### Предварительно установим Docker на ПК под управлением Linux (Ubuntu 22.10), для Windows немного иная установка, тут не рассматриваем:
```bash
sudo apt update && apt upgrade -y
```
### Удаляем старый Docker:
```bash
sudo apt remove docker
```

### Устанавливаем Docker:
```bash
sudo apt install docker.io
```
### Смотрим версию Docker (должно выдать Docker version 20.10.16, build 20.10.16-0ubuntu1):
```bash
docker --version
```
### Активируем Docker в системе, что бы при перезагрузке запускался автоматом:
```bash
sudo systemctl enable docker
```
### Запускаем Docker:
```bash
sudo systemctl start docker
```
### Смотрим статус (выдаст статус, много букв):
```bash
sudo systemctl status docker
```
### Проверим:
```bash
sudo docker run hello-world 
```
### Не будет лишнем установить PostgreSQL:
```bash
sudo apt install postgresql postgresql-contrib -y
```

### Предварительно в папке infra создаем файл .env с следующим содержимом:
```bash
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=postgres 
POSTGRES_USER=postgres 
POSTGRES_PASSWORD=postgres 
DB_HOST=db 
DB_PORT=5432
```

### Так как требование ТЗ и тестов использовать postgresql, то создадим в системе бд, установив локаль:
```bash
sudo dpkg-reconfigure locales 
```
### Выбираем ru_RU.UTF-8 нажав пробел и ждем сообщения Generation complete.
```
Generating locales (this might take a while)...
...
  ru_RU.UTF-8... done
...
Generation complete.
```
### Перезапустим систему:
```bash
sudo reboot
```
### Установка PostgreSQL:
```bash
sudo apt install postgresql postgresql-contrib -y
```
### Управляем БД:
- Остановить
```bash
sudo systemctl stop postgresql
```
```bash
- Запустить
```bash
sudo systemctl start postgresql
```
- Перезапустить
```bash
sudo systemctl restart postgresql
```
- Узнать статус, текущее состояние
```bash
sudo systemctl status postgresql
```
### Создаем бд и пользователя:
```bash
sudo -u postgres psql
```
### Создаем базу:
```sql
CREATE DATABASE test_base;
```
### Создаем пользователя:
```sql
CREATE USER test_user WITH ENCRYPTED PASSWORD 'test_pass';
```
### Даем права для пользователя:
```sql
GRANT ALL PRIVILEGES ON DATABASE test_base TO test_user;
```
### Не забываем про установку, что мы сделали ранее, активировав venv:
```bash
pip install psycopg2-binary
```
```bash
pip install python-dotenv
```
### В settings.py добавляем следующее:
```python
from dotenv import load_dotenv

load_dotenv()

...

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT')
    }
}
```
### Далее в папке где у нас находится файл settings.py создаем файл .env:
```bash
touch .env
```
```bash
nano .env
```
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=test_base
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_pass
DB_HOST=127.0.0.1
DB_PORT=5432
```
### Не забываем про миграции (виртуальное окружение активировано):
```bash
python manage.py migrate
```
### 
Поднимаем контейнеры (
    infra_db - база,
    infra_web - веб,
    nfra_nginx - nginx сервер
    возможно пригодится команда sudo systemctl stop nginx если запускаете в DEV режиме на ПК):
```bash
sudo docker-compose up -d --build 
```