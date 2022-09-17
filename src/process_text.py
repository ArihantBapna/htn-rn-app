from get_transcript import get_transcript
import spacy
import re
import cohere
import annoy

def get_prof_embedding():
    """Returns the embedding of the prof's transcript."""
    api_key = "2LMDM3GEVPLvDVoSQlm4bV5W4EbKn2ZW0jgl6zEM"
    co = cohere.Client(api_key)
    speaker_to_str = get_transcript(filename)
    prof = json_to_lst(speaker_to_str['A'])

    prof_embedding = co.embed(texts=prof,
                               model="large",
                               truncate="RIGHT").embeddings
    return prof_embedding


def json_to_lst(text_content: str):
    # assumption: this is the prof's transcript
    nlp = English()  # just the language with no pipeline
    nlp.add_pipe("sentencizer")
    doc = nlp(text_content)
    text_content = re.sub(r"\(.*\)", "", text_content)
    doc = tokenizer(text_content)
    sentences = [str(x) for x in doc.sents]
    return sentences


def get_title_from_headline(headline: str):
    # get the entity from the headline
    return

# "angular", "euclidean", "manhattan", "hamming", or "dot"
def get_similiar_sentences(prof_embedding, compare):
    # Create the search index, pass the size of embedding
    search_index = AnnoyIndex(prof_embedding.shape[1], 'angular')
    # Add all the vectors to the search index
    for i in range(len(embeds)):
        search_index.add_item(i, embeds[i])

    search_index.build(10) # 10 trees
    search_index.save('transcript.ann')
    # get the similarity between prof and student embeddings
    # return the most similar sentences
    return