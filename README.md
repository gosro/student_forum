# student_forum
Student forum written on Django

## Set up the web site locally
  - Install python3.10
  ```
    sudo apt install python3.10
  ```
  - Install OS components for running Postgres
  ```
  sudo apt update
  sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib build-essential
  ```
  - Create superuser and tables in the db:
  ```
    sudo -u postgres psql

    CREATE DATABASE icef_forum;
    CREATE USER icef_user WITH PASSWORD 'password';
    ALTER ROLE icef_user SET client_encoding TO 'utf8';
    ALTER ROLE icef_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE icef_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE myproject TO icef_user;
  ```
  - Clone with SSH:
  ```
    git clone git@github.com:javitocor/Affiliate-website-Django.git
  ```
  - Go to this repository and set up vurtual environment
  ```
    python3.10 -m venv venv
  ```
  - Install all the requied libraries
  ```
    pip install -r requirements.txt
  ```
  - Work with migrations
  ```
    cd icef_forum
    python3 manage.py makemigrations
    python3 manage.py migrate
  ```
  - Run the program locally
  ```
    python3 manage.py runserver
  ```
