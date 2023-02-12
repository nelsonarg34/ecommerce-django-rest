FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /theungrateful
VOLUME /theungrateful
WORKDIR /theungrateful

RUN apt-get update \
  # psycopg2 dependencies
  && apt-get -y install gcc python3-dev musl-dev \
  # Translations dependencies
  && apt-get -y install gettext \
  # psycopg2https://docs.djangoproject.com/en/4.0/ref/django-admin/
  && apt-get -y install postgresql-client postgresql-client-common\
  # Common dependencies
  && apt-get update && apt-get -y install libpq-dev python3-pip git netcat

# Requirements are installed here to ensure they will be cached.
COPY requirements.txt requirements_dev.txt /rocket_code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /theungrateful/

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

