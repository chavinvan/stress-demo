import pandas as pd
import numpy as np

import re

import contractions
import syntok.segmenter as segmenter

from sentence_transformers import SentenceTransformer

from sklearn.svm import LinearSVC

import pickle

# pre-processing functions

def tokenize(text):
    return '\n\n'.join(
     '\n'.join(' '.join(token.value for token in sentence)
        for sentence in paragraph)
     for paragraph in segmenter.analyze(text))


def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)


def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def create_chatwords_list():
    # read chat words str from file
    chat_words_str = open("data/chatwords.txt", "r").read()

    chat_words_map_dict = {}
    chat_words_list = []
    for line in chat_words_str.split("\n"):
        if line != "":
            cw = line.split("=")[0]
            cw_expanded = line.split("=")[1]
            chat_words_list.append(cw)
            chat_words_map_dict[cw] = cw_expanded
    chat_words_list = set(chat_words_list)
    return chat_words_list, chat_words_map_dict


def chat_words_conversion(text):
    chat_words_list, chat_words_map_dict = create_chatwords_list()

    new_text = []
    for w in text.split():
        if w.upper() in chat_words_list:
            new_text.append(chat_words_map_dict[w.upper()])
        else:
            new_text.append(w)
    return " ".join(new_text)


def expand_contractions(text):
    expanded_words = []   
    for word in text.split():
        # using contractions.fix to expand the shortened words
        expanded_words.append(contractions.fix(word))  
    
    expanded_text = ' '.join(expanded_words)
    return expanded_text




'''
    Preprocess text
'''
text = 'Hello'
text =  remove_urls(text)
text = remove_html(text)
text = chat_words_conversion(text)
text = expand_contractions(text)



'''
    Get embeddings
'''
#model = SentenceTransformer('all-mpnet-base-v2')
#text_embeddings = model.encode(text, show_progress_bar=False).tolist()


'''
    Load model
'''
# load model
##loaded_model = pickle.load(open('model/svm_model.sav', 'rb'))


# predict
#prediction = loaded_model.predict(text_embeddings)
#predi_prob = loaded_model.predict_proba(text_embeddings)




def preprocess(text:str):
    text =  remove_urls(text)
    text = remove_html(text)
    text = chat_words_conversion(text)
    text = expand_contractions(text)

    return text

def get_embedding(text,model):
    return model.encode(text,show_progress_bar=False)

def get_prob(text_embs,loaded_model):
    reshape = text_embs.reshape(1, -1)
    return loaded_model.predict_proba(reshape)

def get_pred(text_embs,loaded_model):
    reshape = text_embs.reshape(1, -1)
    return loaded_model.predict(reshape)
