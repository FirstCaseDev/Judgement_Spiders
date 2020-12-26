import datefinder
import string 
# input_string = "Pradeep Kumar Sonthalia vs Dhiraj Prasad Sahu @ Dhiraj Sahu on 18 December, 2020"
# matches = list(datefinder.find_dates(input_string))
# print (matches[0].month)
s = ",. Basda, ."
# exclude = set(string.punctuation)
# s = ''.join(ch for ch in s if ch not in exclude).strip()

print (s.translate(str.maketrans('', '', string.punctuation)).strip())
