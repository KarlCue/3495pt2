FROM python:3.10-bookworm

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80

ENV NAME analytics-service

CMD ["python", "app.py"]