from typing import Tuple, Set
from get_transcript import get_transcript_from_url
from spacy.lang.en import English
import re
import cohere
import annoy
from flashcard import Flashcard


# filename = "Asking Harvard Students If They Ever Sleep.mp3"
api_key = "2LMDM3GEVPLvDVoSQlm4bV5W4EbKn2ZW0jgl6zEM"
co = cohere.Client(api_key)


def get_prof_data(url):
    """Returns the structured data of the prof's transcript."""
    speaker_to_str = get_transcript_from_url(url)
    transcript = json_to_lst(speaker_to_str["A"])
    print(speaker_to_str)
    entities = speaker_to_str["entities"]
    embedding = co.embed(texts=transcript, model="large", truncate="RIGHT").embeddings
    chapters = speaker_to_str["chapters"]  # (gist, headline, summary)
    return embedding, transcript, entities, chapters


def json_to_lst(text_content: str):
    # assumption: this is the prof's transcript
    text_content = re.sub(r"\(.*\)", "", text_content)
    nlp = English()  # just the language with no pipeline
    nlp.add_pipe("sentencizer")
    doc = nlp(text_content)
    transcript = []
    for sentence in doc.sents:
        transcript.append(sentence.text)
    return transcript


def get_titles_from_chapters(chapter: Tuple[str]) -> str:
    # get the unique keywords for each flashcard from the chapter
    # Query LLM here to give me the key idea based on the chapter gist, summary, and headline
    # ironing out the kinks in prompt generation for now keep it simple and just return the gist
    return chapter[0]


# options for ANN "angular", "euclidean", "manhattan", "hamming", or "dot"
def get_similar_sentences(prof_transcript, prof_embeddings, headlines, n=3):
    phrases_to_vectors = dict(
        zip(prof_transcript, prof_embeddings)
    )  # map our phrases to embeddings

    seen = set()  # seen phrases, prevent duplicate similar sentences
    similar_sentences = {}  # key: headline, value: (headline embedding, list of top 3 phrases, list of embeddings)

    search_index = annoy.AnnoyIndex(
        prof_embeddings.shape[1], "angular"
    )  # build ANN search tree
    for i in range(len(prof_embeddings)):
        search_index.add_item(i, prof_embeddings[i])
    search_index.build(10)  # 10 trees

    # search_index.save('transcript.ann') # we can save this tree if needed later

    # get the similarity between prof and headline embedding
    for headline in headlines:
        headline_embedding = co.embed(
            texts=[headline], model="large", truncate="RIGHT"
        ).embeddings
        similar_sentences[headline] = (headline_embedding, [], [])

    for i in range(n):
        for headline in headlines:
            top = search_index.get_nns_by_vector(similar_sentences[headline][0][0], 1)[0]
            if top in seen:
                j = 1
                while top in seen:
                    top = search_index.get_nns_by_vector(
                        similar_sentences[headline][0][0], j)[j]
                    j += 1
            seen.add(top)
            similar_sentences[headline][1] += top
            similar_sentences[headline][2] += phrases_to_vectors[top]

    return similar_sentences


def get_flashcards(url) -> Set[Flashcard]:
    # get the transcript and relevant data
    prof_data = get_prof_data(url)  # (transcript, embeddings, entities, chapters)
    prof_transcript = prof_data[0]
    prof_embeddings = prof_data[1]
    entities = prof_data[2]
    chapters = prof_data[3]
    # get the chapters, get the unique titles from each chapter
    titles = [get_titles_from_chapters(c) for c in chapters]
    headlines = [c[1] for c in chapters]
    # get the similar sentences to each headline
    similar_sentences = get_similar_sentences(
        prof_transcript, prof_embeddings, headlines
    )
    # ^^^ key: headline, value: (headline embedding, list of top 3 phrases, list of embeddings)
    flashcards = set()
    for t in titles:
        sents = "\n".join(similar_sentences[1])
        back = f"{headlines}\n{sents}"
        embedding = co.embed(texts=[back], model="large", truncate="RIGHT").embeddings
        flashcards.add(
            Flashcard(
                t,
                back,
                chapters[0],
                None,
                None,
                headlines,
                similar_sentences[0],
                similar_sentences,
                embedding[0]
            )
        )
    # init flashcard: need front: str
    # back: str
    # gist: str
    # first: Union[None, str]
    # second: Union[None, str]
    # headline: str
    # _headline_embedding: list
    # _embedding: list

    return flashcards
