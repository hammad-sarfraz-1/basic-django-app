🛡️ Django Authentication Project
A simple Django project with login, signup, and logout functionality using PostgreSQL and Django REST Framework.

📦 Technologies Used
Django 5.2

Django REST Framework

PostgreSQL

HTML Templates

🛠️ Setup Instructions
1. Clone the Repository

            git clone s://github.com/yourusername/django-auth-project.git
cd django-auth-project
2. Set Up Virtual Environment
            python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
            pip install -r requirements.txt
🗃️ Database Configuration (PostgreSQL)
In your PostgreSQL terminal:

        CREATE DATABASE mydb;
        CREATE USER myuser WITH PASSWORD 'mypassword';
        GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
In settings.py, update the DATABASES config:

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'mydb',
                'USER': 'myuser',
                'PASSWORD': 'mypassword',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
🚀 Run the Project

        python manage.py makemigrations
        python manage.py migrate
        python manage.py createsuperuser  # Follow prompts
        python manage.py runserver
    Visit: ://127.0.0.1:8000/accounts/signup/

🔐 API Endpoints
        Method	Endpoint	Description
        POST	/accounts/api/signup/	API for user signup
        POST	/accounts/api/login/	API for user login
        GET	/accounts/home/	Home page (protected)

🛡️ CSRF Trusted Origins
Add the following to your settings.py:


        CSRF_TRUSTED_ORIGINS = [
            '://localhost:8000',
            '://127.0.0.1:8000'
        ]
Make sure {% csrf_token %} is included inside all HTML <form> elements.

🧾 Example API Requests
Signup

POST /accounts/api/signup/

Content-Type: application/json

{
  "username": "john",
  "password": "test1234",
  "email": "john@example.com"
}

Login

POST /accounts/api/login/
Content-Type: application/json

{
  "username": "john",
  "password": "test1234"
}
🧰 Project Structure



    project/
    │
    ├── accounts/
    │   ├── views.py
    │   ├── urls.py
    │   └── templates/accounts/
    ├── manage.py
    ├── db.sqlite3
    ├── requirements.txt
    └── README.md
