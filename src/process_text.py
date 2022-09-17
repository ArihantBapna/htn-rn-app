import get_transcript
import spacy
import cohere


transcript = generate_prof_transcript(filename)

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
    # re.sub the question tags fjdlkfldkfj (X) sfjdlfdk
    doc = nlp(text_content)
    sentences = [str(x) for x in doc.sents]
    print(sentences)
    return sentences