from get_prof_transcript import generate_prof_transcript
import spacy
import re
import cohere


def get_prof_embedding(speaker_to_str: dict):
    '''Returns the embedding of the prof's transcript.'''
    api_key = "2LMDM3GEVPLvDVoSQlm4bV5W4EbKn2ZW0jgl6zEM"
    co = cohere.Client(api_key)
    transcript = generate_prof_transcript(filename)
    # get lst of speaker A's sentences
    prof = json_to_lst(speaker_to_str['A'])

    prof_embeddings = co.embed(texts=prof,
                               model="large",
                               truncate="RIGHT").embeddings
    return prof_embeddings


def json_to_lst(text_content: str):
    # assumption: this is the prof's transcript
    nlp = spacy.load("en_core_web_sm", disable=["ner"])
    text_content = re.sub(r"\(.*\)", "", text_content)
    doc = nlp(text_content)
    sentences = [str(x) for x in doc.sents]
    print(sentences)
    return sentences

def get_entity_from_headline(headline: str):
    # get the entity from the headline
    return

def get_similiar_sentences(prof, compar):
    # get the similarity between prof and student embeddings
    # return the most similar sentences
    return