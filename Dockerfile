FROM python:3.10.2-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN  mkdir -p /opt/app/static/ \
    && mkdir -p /opt/app/media/ \
    && mkdir -p /var/lib/postgresql/data/ \
    && python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY ./app/ .

EXPOSE 8080/tcp

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8080" ]


