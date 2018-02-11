FROM python:3.6.4-alpine3.6
MAINTAINER David Krauth "dakrauth@gmail.com"

COPY requirements /app/requirements
RUN pip install -r /app/requirements/dev.txt 

COPY . /app
WORKDIR /app/demo

RUN pip install -e ../
RUN python manage.py loaddemo

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0:80"]

