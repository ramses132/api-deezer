FROM python:3.8

WORKDIR /app

RUN wget -q https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -P /usr/local/bin \
&& chmod +x /usr/local/bin/wait-for-it.sh \
&& mkdir -p /app \
&& useradd -u 901 -r api-deezer --create-home \
# all project specific folders need to be accessible by newly created user but also for unknown users (when UID is set manually). Such users are in group root.
&& chown -R api-deezer:root /home/api-deezer \
&& chmod -R 770 /home/api-deezer


RUN apt-get update && apt-get install -y --no-install-recommends \
  # needed for psycopg2
  libpq-dev

# needs to be set for users with manually set UID
ENV HOME=/home/api-deezer

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE api-deezer.settings
ENV APP_HOME=/app
ENV UWSGI_INI /app/uwsgi.ini

ARG REQUIREMENTS=requirements.txt
COPY requirements.txt requirements-dev.txt $APP_HOME/
RUN pip install --upgrade --no-cache-dir --requirement $REQUIREMENTS --disable-pip-version-check

USER api-deezer

COPY . $APP_HOME

EXPOSE 8000

CMD /bin/sh -c "wait-for-it.sh $DATABASE_HOST:${DATABASE_PORT:-5432} -- ./manage.py migrate && uwsgi"
