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
## 3: Set up memcached:
#### Install and start daemon memcached:
```bash
sudo apt-get install memcached

service memcached start
```
#### Restart daemon and clear memcached:
```bash
service memcached restart
```
## 4: Getting Started
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
#### Inside the project directory set the initial data with fixtures:
#### Attention! Be sure to run the commands in the order shown.
```bash
python manage.py loaddata users.json

python manage.py loaddata categories.json

python manage.py loaddata ads.json

python manage.py loaddata images.json 
```
#### Users:
```bash
Admin: 
username: "admin" 
password: "123" 

Max: 
username: "Max"
password: "12345678max"

John: 
username: "John"
password: "12345678john"

Alex: 
username: "Alex"
password: "12345678alex"
```
## 5: Run Celery Tasks:
### Running Locally:
#### Install Redis as a Celery “Broker” in your system, not in virtualenv:
```bash
wget http://download.redis.io/redis-stable.tar.gz

tar xvzf redis-stable.tar.gz

cd redis-stable

make
```
#### Check installation:
```bash
redis-server
```
##### With your running Django App and running Redis, open two new terminal windows/tabs. 
##### Activate your virtualenv in each new window, navigate to root project directory where
##### "my_ad" folder and manage.py file are located, and then run the following commands (one in each window):
```bash
celery -A my_ad worker -l info

celery -A my_ad beat -l info
```

