import datefinder
import string 
import pymongo
import json
# input_string = "Pradeep Kumar Sonthalia vs Dhiraj Prasad Sahu @ Dhiraj Sahu on 18 December, 2020"
# matches = list(datefinder.find_dates(input_string))
# print (matches[0].month)
# s = ",. Basda, ."
# exclude = set(string.punctuation)
# s = ''.join(ch for ch in s if ch not in exclude).strip()

# print (s.translate(str.maketrans('', '', string.punctuation)).strip())

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["US_SCdata"]
col = db["US_SupremeCourt"]
with open('C:/Users/punee/Downloads/scotus/87116.json') as file:
        file_data=json.load(file)

print (file_data)
if isinstance(file_data,list):
    col.insert_many(file_data)
else:
    col.insert_one(file_data)

# x = col.find({'year': 2020, 'month': 12},{'url': 1, 'year': 1, 'month': 1})

# for a in x:
#     print (a['url'])