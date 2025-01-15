FROM python:3.9-alpine

WORKDIR /code

# Installa dipendenze di build temporanee
RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev libffi-dev openssl-dev

COPY requirements.txt /code

# Aggiorna pip e installa i pacchetti
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

# Copia il codice
COPY app app
COPY model_artifacts model_artifacts

# Rimuove i pacchetti di build per ridurre le dimensioni finali
RUN apk del .build-deps

EXPOSE 80

# Esempio di comando per avviare FastAPI con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]