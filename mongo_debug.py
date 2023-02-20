import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gpt_test"]
col = db["gpt_col_test"]

data = {"name": "John", "age": 30}
col.insert_one(data)