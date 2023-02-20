import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["gpt_test"]
col = db["gpt_col_test"]

cursor = col.find()
for doc in cursor:
    print(doc)