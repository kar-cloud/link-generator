# Link Generator - Backend

The backend of this application has been built using Django, DRF, MySQL.
<br>
You can find frontend for this application through this repository: [Frontend](https://github.com/kar-cloud/Link-generator-frontend)
<br>
The project has been deployed on Vercel: [Link](https://link-generator-frontend.vercel.app/)

## Installation Locally Steps

Pre-requisite of this project is to have Python3.10 and pip installed on your system.
<br>

### `git clone https://github.com/kar-cloud/link-generator.git`
<br>

Generate a virtual enviroment
### `python -m venv venv`
### `source venv/bin/activate`
<br>

Install the requirements
### `pip install -r requirements.txt`
<br>

Create <b>.env</b> in the root folder of the project. <br>
Add these configurations in .env file:

SECRET_KEY=<br>
DATABASE_NAME=<br>
DATABASE_USERNAME=<br>
DATABASE_PASSWORD=<br>
DATABASE_HOST=<br>
DATABASE_PORT=<br>
JWT_SECRET=<br>
<br>

Dont put space anywhere= sign. For example, SECRET_KEY=abc_ee <br>
<br>

If you have not created MYSQL database, create one using command in mysql shell: <b>create database <database_name></b><br>
Run commands for migrations to apply:
<br>
### `python manage.py makemigrations`
### `python manage.py migrate`
<br>

Finally run the server
### `python manage.py runserver`
