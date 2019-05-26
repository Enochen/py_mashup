import spacy
import wikipedia
import random
from flask import jsonify


def __random_summary():
   random = wikipedia.random(1)
   try:
       result = wikipedia.page(random).summary.encode("utf-8")
   except:
       result = __random_summary()
   return result
   
def __search(list, token):
    random.shuffle(list)
    for i in range(len(list)):
        if list[i].tag_ == token.tag_ and not token.left_edge.text == list[i].text and not token.right_edge.text == list[i].text and not (token.text[0].isupper() and not list[i].text[0].isupper()):
            if not (token.is_digit and not token.shape_ == list[i].shape_):
                return i
    else:
        return -1

def __remove_dup(list):
    seen = set()
    result = []
    for token in list:
        if token.text not in seen:
            result.append(token)
            seen.add(token.text)
    return result

def mashup(**kwargs):
    origin = ''
    modifier = ''
    
    if "origin" in kwargs and not kwargs['origin'] == '':
        origin = kwargs['origin']
    else:
        origin = __random_summary().decode("utf-8")
        
    if "modifier" in kwargs and not kwargs['modifier'] == '':
        print(modifier)
        modifier = kwargs['modifier']
    else:
        modifier = __random_summary().decode("utf-8")

    nlp = spacy.load('en_core_web_sm')
    doc_origin = nlp(origin)
    doc_modifier = nlp(modifier)

    all_words = []

    for token in doc_modifier:
        if not token.is_stop:
            all_words.append(token)

    words = __remove_dup(all_words)

    str = ''
    for token in doc_origin:
        sub = token.text
        index = __search(words, token)
        if not token.is_stop and random.random() < 1 and index > -1:
            sub = words.pop(index).text
        str += sub;
        if token.whitespace_:
            str += ' '
    return (origin, modifier, str)