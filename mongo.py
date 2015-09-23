
from pymongo import MongoClient
import config
import datetime


client = MongoClient(config.HOST, 27017)
db = client[config.DB_NAME]




