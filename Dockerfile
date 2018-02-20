FROM python:3.6-alpine

MAINTAINER Kosenko Artyom <kosc@hotkosc.ru>

COPY requirements.txt /chatquotes/requirements.txt
WORKDIR /chatquotes
RUN pip install -r requirements.txt
COPY migrations migrations
COPY templates templates
COPY app.py .
ENTRYPOINT ["python", "app.py"]
CMD ["runserver"]
