FROM python:3.6.4-alpine3.6
WORKDIR /app
COPY requirements ./requirements
COPY swingtime ./swingtime
COPY demo .
RUN pip install -r requirements/dev.txt \
    && python manage.py loaddemo

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0:80"]

