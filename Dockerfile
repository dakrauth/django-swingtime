FROM python:3.6.4-alpine3.7
MAINTAINER David Krauth "dakrauth@gmail.com"

COPY . /app
COPY requirements /app/requirements
WORKDIR /app
RUN pip install -r /app/requirements/dev.txt 

WORKDIR /app/demo

RUN pip install -e ../
RUN python manage.py loaddemo

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0:80"]

