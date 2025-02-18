FROM python:3.9


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app
COPY ./model_artifacts /code/model_artifacts


CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "80"]