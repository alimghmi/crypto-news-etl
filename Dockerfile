FROM python:3

COPY . /app

WORKDIR /app

RUN pip install requirements.txt

CMD [ "python", "app.py" ]