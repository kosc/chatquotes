FROM python:3.6-alpine

COPY requirements.txt /chatquotes/requirements.txt
WORKDIR /chatquotes
RUN pip install -r requirements.txt
COPY migrations .
COPY templates .
COPY app.py .
RUN python app.py migrate
