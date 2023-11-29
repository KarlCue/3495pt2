from sqlalchemy import Column, DateTime, Integer, Float
from base import Base

class Temperature(Base):
    """ Temperature """

    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)

    def __init__(self, max_temp, min_temp, timestamp):
        """ Initializes a temperature reading """
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.timestamp = timestamp

    def to_dict(self):
        dict = {}
        dict["id"] = self.id
        dict["max_temp"] = self.max_temp
        dict["min_temp"] = self.min_temp
        dict["timestamp"] = self.timestamp
        return dict