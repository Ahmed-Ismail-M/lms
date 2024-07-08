FROM python:latest
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements.txt /code/
COPY ./lms /code/
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["sh", "-c", "python manage.py makemigrations library && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
