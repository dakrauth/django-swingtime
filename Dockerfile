FROM python:3.13-alpine
LABEL org.opencontainers.image.author="dakrauth@gmail.com"

COPY . /app
RUN pip install "/app[dev]"
WORKDIR /app/demo

RUN python manage.py migrate

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0:80"]

