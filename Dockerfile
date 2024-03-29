FROM python:3.11

WORKDIR /app/

COPY ./workflow_engine /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
