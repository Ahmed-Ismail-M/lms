FROM python:latest

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./lms /code/

EXPOSE 8000

ENTRYPOINT ["/code/django.sh"]

# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
