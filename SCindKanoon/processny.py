import re 
import regex
import pymongo 

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["US_SCdata"]
col = db["US_SCdata04"]

count = 0
for count, doc in enumerate(col.find()):
    url = doc['url']
    respondent_counsel = doc['respondent_counsel']
    new = []
    new.append(respondent_counsel)
    print(respondent_counsel)
    print(new)
    print(count+1)
    print(".................")
    col.update_one({"url": url},{"$set": {"respondent_counsel":new}}, False, True)

    
