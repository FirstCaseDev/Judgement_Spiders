import re 
import regex
import pymongo 
from string import punctuation

client = pymongo.MongoClient("mongodb+srv://PuneetShrivas:admin@betatesting.nsnxl.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client["courtdata"]
col = db["cases"]
act_name_patterns = 'act|law|constitution|rule|notification|circular|paragraph|article|statute|reference|section|interpretation|regulation|regulations'
count = 0
for count, doc in enumerate(col.find({"$and":[{"source":"Supreme Court of India"},{"provisions_referred":{"$exists":"true"}}]})):
    provisions_string = doc['provisions_referred']
    title = doc['title']
    print('.......')
    if type(provisions_string) == str:
        provisions_array = []
        for act in provisions_string.split(';'):
            act_splits = re.split('[|:]',act)
            act_splits = [i for i in act_splits if i]
            if len(act_splits):
                act_name = act_splits[0].strip(punctuation)
                if  re.search(act_name_patterns,act_name,re.IGNORECASE) == None : 
                    print('Act_name ommited: ' + act_name + '..........')
                    print(act_splits)
                    continue
                act_sections = act_splits[1:]
                ommit_sections = []
                for section in act_sections:
                    if re.search(r"S\.|s\.|S\. |s\. |rule",section,re.IGNORECASE) != None : 
                        if re.search(r"\d+", section) == None :
                            print(act_name + "'s section ommited: " + section)
                            ommit_sections.append(section)
                for section in ommit_sections:
                    while section in act_sections:
                            act_sections.remove(section)
                act_sections = list(set(act_sections)) 
                provisions_array.append({"act_name": act_name, "act_sections": act_sections})  
        print(title)
        print('............................')
        print(count)
        col.update_one({"title": title},{"$set": {"provisions_referred":provisions_array }}, False, True)
    else:
        print(title + "'s  provisions_referred is NOT a string")
    print(count+1)

    # url = doc['url']
    # respondent_counsel = doc['respondent_counsel']
    # new = []
    # new.append(respondent_counsel)
    # print(respondent_counsel)
    # print(new)
    # print(count+1)
    # print(".................") {"source": "Supreme Court of India"}
    # col.update_one({"url": url},{"$set": {"respondent_counsel":new}}, False, True)

    
