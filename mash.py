import spacy
import wikipedia
import random
from flask import jsonify
import en_core_web_sm

nlp = en_core_web_sm.load()

def __random_summary(min, max):
    random = wikipedia.random(10)
    try:
        for i in range(10):
            result = wikipedia.page(random[i]).summary.encode('utf-8')
            length = len(result)
            if length > min and length < max:
                break
    except:
        return __random_summary(min, max)
    return result.decode('utf-8')


def __search(list, token):
    random.shuffle(list)
    for i in range(len(list)):
        if list[i].tag_ == token.tag_ and not (token.text[0].isupper()
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
    
def __gen_sen(doc, words, craziness):
    temp_words = words[:]
    str = ''
    for token in doc:
        sub = token.text
        index = __search(temp_words, token)
        if not token.is_stop and random.random() < craziness and index \
            > -1:
            sub = temp_words.pop(index).text
        str += sub
        if token.whitespace_:
            str += ' '
    return nlp(str)


def __get_similarity(doc1, doc2, doc3):
    print()
    print("FINAL:", doc1.text)
    print()
    s12 = doc1.similarity(doc2)
    s23 = doc1.similarity(doc3)
    print("Similarity 1-2-3:", s12 + s23)
    print()
    return s12 + s23;
    
def __diff(doc1, doc2):
    d = 0
    print(len(doc1), 'vs', len(doc2))
    for i in range(len(doc1)):
        if(doc1[i].tag_ != doc2[i].tag_):
            d += 1
    return d

def random_wiki():
    return __random_summary(0, 1500)

def mashup(**kwargs):
    print("starting")
    original = ''
    modifier = ''
    craziness = 100

    if 'original' in kwargs and not kwargs['original'] == '':
        original = kwargs['original']
    else: 
        original = __random_summary(500, 1000)
        #original = __random_summary(0, 1500)
        print("finished fetching o: length =", len(original))

    if 'modifier' in kwargs and not kwargs['modifier'] == '':
        modifier = kwargs['modifier']
    else:
        #modifier = __random_summary(len(original)-100, len(original)+200)
        modifier = __random_summary(len(original), 1500)
        print("finished fetching m: length =", len(modifier))

    if 'craziness' in kwargs and not kwargs['craziness'] == '':
        craziness = kwargs['craziness']
    doc_original = nlp(original)
    doc_modifier = nlp(modifier)

    words = []

    for token in doc_original:
        if not token.is_stop:
            words.append(token)
    for token in doc_modifier:
        if not token.is_stop:
            words.append(token)

    words = __remove_dup(words)

    print("Original:", doc_original.text)
    print()
    print("Modifier:", doc_modifier.text)
    print()
    
    sentences = []
    for i in range(100):
        sentences.append(__gen_sen(doc_original, words, craziness))
    best = max(sentences, key=lambda x: doc_original.similarity(x))
    return (original, modifier, best.text)
	
#print(mashup()[2].encode('utf-8'))
