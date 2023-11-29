import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
from base import Base
from temperature import Temperature
from create_tables import create_tables

app = Flask(__name__)
host=os.environ.get("MYSQL_HOST", "127.0.0.1")
port=int(os.environ.get("MYSQL_PORT", "3306"))
password=os.environ.get("MYSQL_PASSWORD", "password")
user=os.environ.get("MYSQL_USER", "root")
database=os.environ.get("MYSQL_DATABASE", "data-db")

DB_ENGINE = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

@app.get("/")
def get_index():
    return render_template("index.html")

@app.post("/enter-data")
def post_enter_data():
    form = request.form

    response = requests.post(os.environ.get("AUTH_URL", "http://127.0.0.1:3000/"), data={ "username": form["username"], "password": form["password"] })
    if response.status_code != 200:
        return f"Failed to Authenticate: {response.json()['message']}"

    if not form["date"]:
        return "No date provided."
    
    if not form["min_temp"]:
        return "No min_temp provided."
    
    if not form["max_temp"]:
        return "No max_temp provided."

    if form["max_temp"] < form["min_temp"]:
        return "Max temp must be greater than min temp."
    
    with DB_SESSION() as session:
        session = DB_SESSION()
        temperature = Temperature(form["max_temp"], form["min_temp"], form["date"])

        session.add(temperature)
        session.commit()

    return "Successfully inserted temperature data."

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=5000)