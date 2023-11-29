import datetime
import os
import time
from pymongo import MongoClient
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from temperature import Temperature
from base import Base

mysql_host=os.environ.get("MYSQL_HOST", "127.0.0.1")
mysql_port=int(os.environ.get("MYSQL_PORT", "3306"))
mysql_password=os.environ.get("MYSQL_PASSWORD", "password")
mysql_user=os.environ.get("MYSQL_USER", "root")
mysql_database=os.environ.get("MYSQL_DATABASE", "data-db")

mongo_host=os.environ.get("MONGO_HOST", "127.0.0.1")
mongo_port=int(os.environ.get("MONGO_PORT", "27017"))
mongo_pass=os.environ.get("MONGO_PASSWORD", "pass")
mongo_user=os.environ.get("MONGO_USER", "user")
print(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}")
print(f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}")
DB_ENGINE = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_database}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

client = MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}")
mongo_db = client["results"]

def calculate_statistics():
    print("Calculating statistics...")
    session = DB_SESSION()

    temperatures = session.query(Temperature).all()
    avg_min = []
    avg_max = []
    for temp in temperatures:
        avg_min.append(temp.min_temp)
        avg_max.append(temp.max_temp)

    avg_min = sum(avg_min) / len(avg_min)
    avg_max = sum(avg_max) / len(avg_max)
    
    mongo_db.results_collection.insert_one({ "avg_min": avg_min, "avg_max": avg_max, "time": datetime.datetime.now() })
    print("Finished calculating statistics.")


if __name__ == "__main__":
    while True:
        calculate_statistics()
        time.sleep(10)