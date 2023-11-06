FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir pymongo

RUN pip install --no-cache-dir flake8

RUN flake8 --ignore=E501,F401 .

EXPOSE 5000

ENV FLASK_APP=server/endpoints.py

ENV MONGO_URI mongodb://your-db-uri

CMD ["flask", "run", "--host=0.0.0.0"]
