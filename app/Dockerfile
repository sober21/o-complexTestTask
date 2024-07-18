FROM python:3.11-alpine

WORKDIR /app

ENV FLASK_APP=run.py

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "flask","run", "--host=0.0.0.0", "--port=8000" ]