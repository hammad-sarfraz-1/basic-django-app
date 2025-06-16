# python image
FROM python:3.11-slim



# environment variables

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# working directory
WORKDIR /app

# dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt


# copy project files
COPY . .

# port exposing
EXPOSE 8000

# run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
