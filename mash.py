import spacy
import wikipedia
import random
from flask import jsonify
import en_core_web_sm


def __random_summary():
    random = wikipedia.random(1)
    try:
        result = wikipedia.page(random).summary.encode('utf-8')
        if result.length < 600:
            result = __random_summary()
    except:
        result = __random_summary()
    return result


def __search(list, token):
    random.shuffle(list)
    for i in range(len(list)):
        if list[i].tag_ == token.tag_ and not token.left_edge.text \
            == list[i].text and not token.right_edge.text \
            == list[i].text and not (token.text[0].isupper()
                and not list[i].text[0].isupper()):
            if not (token.is_digit and not token.shape_
                    == list[i].shape_):
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
    original = __random_summary().decode('utf-8')
    modifier = __random_summary().decode('utf-8')
    craziness = 100

    if 'original' in kwargs and not kwargs['original'] == '':
        original = kwargs['original']

    if 'modifier' in kwargs and not kwargs['modifier'] == '':
        modifier = kwargs['modifier']

    if 'craziness' in kwargs and not kwargs['craziness'] == '':
        craziness = kwargs['craziness']

    nlp = en_core_web_sm.load()
    doc_origin = nlp(original)
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
        if not token.is_stop and random.random() < craziness and index \
            > -1:
            sub = words.pop(index).text
        str += sub
        if token.whitespace_:
            str += ' '
    return (original, modifier, str)