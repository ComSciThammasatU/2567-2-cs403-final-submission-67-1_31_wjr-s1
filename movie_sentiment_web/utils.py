
import re
from bs4 import BeautifulSoup
import contractions
import nltk
from nltk.corpus import stopwords
import spacy

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

def clean_text(text):
    text = text.lower()
    text = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", '', text)
    for key, value in contractions.contractions_dict.items():
        text = text.replace(key, value)
    text = BeautifulSoup(text, 'html.parser').get_text().strip()
    text = re.sub(r'[^\w ]+', "", text)
    text = ' '.join(text.split())
    text = ' '.join([word for word in text.split() if word not in stop_words])
    doc = nlp(text)
    lemmas = [token.lemma_ if token.lemma_ not in ['-PRON-', 'be'] else token.text for token in doc]
    return ' '.join(lemmas)

def clean_texts(texts):
    return [clean_text(t) for t in texts]
