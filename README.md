# Django "My Ad" web app.

## 1: Initial Setup

#### Clone project in a new directory:
```bash
cd path/to/a/new/directory

git clone https://github.com/MaksNech/django_my_ad.git
```
## 2: Install PostgreSQL:
```bash
sudo apt-get update

sudo apt-get install postgresql
```
#### Or follow the installation instructions for PostgreSQL from the official website:
https://www.postgresql.org/download

#### Check installation:
```bash
sudo -u postgres psql
```
#### Create app database:
```bash
CREATE DATABASE my_ad_db;
```

#### Or exit from postgres command line and create db with linux command:
```bash
\q

sudo -u postgres createdb my_ad_db
```

#### Enter to the database:
```bash
sudo -u postgres psql -d my_ad_db
```

#### Create user of the db from postgres command line:
```bash
CREATE USER admin WITH PASSWORD '123';

\q
```
#### Go to the postgres command line and do some customization:
```bash
sudo -u postgres psql

ALTER ROLE admin SET client_encoding TO 'utf8';

ALTER ROLE admin SET default_transaction_isolation TO 'read committed';

ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE my_ad_db TO admin;

ALTER USER admin CREATEDB;

\q
```

## 3: Getting Started

### Start backend:
#### Inside project create virtual environment:
```bash
virtualenv -p python3 env
```
#### Then start virtual environment:
```bash
source env/bin/activate
```
#### Install packages using pip according to the requirements.txt file:
```bash
pip3 install -r requirements.txt
```
#### Inside the project directory migrate the database:
```bash
python manage.py makemigrations

python manage.py migrate
```

