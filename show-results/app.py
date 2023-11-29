import os
from flask import Flask, render_template, request
from pymongo import MongoClient
import pymongo
import requests

mongo_host=os.environ.get("MONGO_HOST", "127.0.0.1")
mongo_port=int(os.environ.get("MONGO_PORT", "27017"))
mongo_pass=os.environ.get("MONGO_PASSWORD", "pass")
mongo_user=os.environ.get("MONGO_USER", "user")

app = Flask(__name__)
client = MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}")
mongo_db = client["results"]

@app.get("/")
def get_index():
    return render_template("index.html")

@app.post("/login")
def post_enter_data():
    form = request.form
    response = requests.post(os.environ.get("AUTH_URL", "http://127.0.0.1:3000/"), data={ "username": form["username"], "password": form["password"] })
    if response.status_code != 200:
        return f"Failed to Authenticate: {response.json()['message']}"

    data = mongo_db.results_collection.find_one(sort=[( 'time', pymongo.DESCENDING )])

    return f"""
        <h1>Average Temperatures</h1>
        <p>Average Minimum Temperature: {data["avg_min"]}</p>
        <p>Average Maximum Temperature: {data["avg_max"]}</p>
        <p>Data last updated: {data["time"]}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)