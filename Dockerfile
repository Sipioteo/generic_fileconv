FROM python:3.9-alpine

WORKDIR /code

# Install build dependencies if needed (gcc, musl-dev, etc.)
RUN apk add --no-cache gcc musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app ./app
COPY ./model_artifacts ./model_artifacts

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]