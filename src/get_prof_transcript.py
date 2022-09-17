import cohere
import pandas as pd
from sklearn.model_selection import train_test_split
from load_audio import get_response
from tqdm import tqdm
import spacy
import re

filename = "Asking Harvard Students If They Ever Sleep.mp3"


def generate_prof_transcript(file):
    # assumption: speaker A is the prof <3
    response_json = get_response(file)
    speakers = response_json['utterances']

    speaker_to_str = {}
    for d in speakers:   # speaker, text
        if d['speaker'] not in speaker_to_str:
            speaker_to_str[d['speaker']] = d['text']
            if d['speaker'] != 'A':
                speaker_to_str['A'] += f'(speaker: {d["speaker"]})'  # marking who's Q it was
        else:
            speaker_to_str[d['speaker']] += ('\n' + d['text'])
    print(speaker_to_str)
    return speaker_to_str


def get_prof_embedding(speaker_to_str):
    # assumption: only want embeddings of the prof's lecture
    pd.set_option('display.max_colwidth', None)

    # get lst of speaker A's sentences
    test = json_to_lst(speaker_to_str['A'])

    # get embeddings
    api_key = "2LMDM3GEVPLvDVoSQlm4bV5W4EbKn2ZW0jgl6zEM"
    co = cohere.Client(api_key)
    embeddings_test = co.embed(texts=test,
                               model="large",
                               truncate="LEFT").embeddings
    return embeddings_test


def json_to_lst(text_content: str):
    # assumption: this is the prof's transcript
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    text_content = re.sub("\(.*\)", '', text_content)
    doc = nlp(text_content)
    sentences = [str(sent) for sent in doc.sents]
    print(len(sentences))
    return sentences

