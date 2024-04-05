FROM python:3.11-bullseye
WORKDIR /ems
COPY requirements.txt /ems/
RUN pip install -r requirements.txt
COPY . /ems/
CMD celery -A ems worker --loglevel=info & python manage.py runserver 0.0.0.0:8000
EXPOSE 8000