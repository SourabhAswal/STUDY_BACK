FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && pip3 install --upgrade pip && apt-get install python3-dev default-libmysqlclient-dev build-essential -y
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
VOLUME /app/data
EXPOSE 8000
CMD exec gunicorn --bind 0.0.0.0:8000 SkillBuilder_LMSBackend.wsgi
