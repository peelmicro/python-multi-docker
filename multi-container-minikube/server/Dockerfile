FROM python:3-alpine

WORKDIR /app

COPY requirements.txt .

# https://stackoverflow.com/a/47871121/1059286
RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


COPY . .

CMD ["python3", "app.py"]