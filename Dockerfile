FROM python:3.12.7-alpine
MAINTAINER David Krauth "dakrauth@gmail.com"

COPY . /app
WORKDIR /app/demo
RUN pip install ../

RUN python manage.py loaddemo

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0:80"]

