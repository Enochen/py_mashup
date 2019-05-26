import spacy
import wikipedia
import random
from flask import jsonify


def random_summary():
   random = wikipedia.random(1)
   try:
       result = wikipedia.page(random).summary
   except wikipedia.exceptions.DisambiguationError as e:
       result = random_summary()
   return result
   
def search(list, token):
    random.shuffle(list)
    for i in range(len(list)):
        if list[i].tag_ == token.tag_ and not token.left_edge.text == list[i].text and not token.right_edge.text == list[i].text and not (token.text[0].isupper() and not list[i].text[0].isupper()):
            if not (token.is_digit and not token.shape_ == list[i].shape_):
                return i
    else:
        return -1

def remove_dup(list):
    seen = set()
    result = []
    for token in list:
        if token.text not in seen:
            result.append(token)
            seen.add(token.text)
    return result


nlp = spacy.load('en_core_web_sm')
origin = nlp(random_summary())
modifier = nlp(random_summary())

all_words = []

for token in modifier:
    if not token.is_stop:
        all_words.append(token)

words = remove_dup(all_words)

str = ''
for token in origin:
    sub = token.text
    index = search(words, token)
    if not token.is_stop and random.random() < 1 and index > -1:
        sub = words.pop(index).text
    str += sub;
    if token.whitespace_:
        str += ' '
        
print(jsonify(origin=origin, modifier=modifier, result=str))