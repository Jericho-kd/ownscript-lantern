FROM python:3.10-slim

RUN mkdir /app

COPY . /app
COPY pyproject.toml /app

WORKDIR /app
RUN touch README.md

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 9999

WORKDIR /app/ownscript_lantern

ENTRYPOINT ["python3", "main.py"]