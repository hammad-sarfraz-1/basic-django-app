# Django Authentication Project

A simple Django project with login, signup, and logout functionality using PostgreSQL and Django REST Framework.

## Technologies Used

- Django 5.2
- Django REST Framework
- PostgreSQL
- HTML Templates

## Setup Instructions

1. Clone the Repository

```bash
git clone https://github.com/yourusername/django-auth-project.git
cd django-auth-project
```

2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Database Configuration (PostgreSQL)

In your PostgreSQL terminal:

```sql
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
```

In `settings.py`, update the `DATABASES` config:

```python
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
```

## Run the Project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Follow prompts
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/accounts/signup/](http://127.0.0.1:8000/accounts/signup/)



## CSRF Trusted Origins

Add the following to your `settings.py`:

```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000'
]
```

Make sure `{% csrf_token %}` is included inside all HTML `<form>` elements.

##  Project Structure

```
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
