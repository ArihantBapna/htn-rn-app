from typing import Tuple, Set
from get_transcript import get_transcript_from_url
from spacy.lang.en import English
import re
import json
import cohere
import annoy
from flashcard import Flashcard
from main import cohere_api

co = cohere.Client(cohere_api)


def get_prof_data(url):
    """Returns the structured data of the prof's transcript."""
    speaker_to_str = json.loads(get_transcript_from_url(url))
    try:
        transcript = json_to_lst(speaker_to_str["A"])
    except KeyError:
        transcript = json_to_lst(speaker_to_str["UNK"])
    entities = speaker_to_str["entities"]
    embedding = co.embed(texts=transcript, model="large", truncate="RIGHT").embeddings
    chapters = speaker_to_str["chapters"]  # (gist, headline, summary)
    return transcript, embedding, entities, chapters


def json_to_lst(text_content: str):
    """Converts a json transcript to a list of strings."""
    # assumption: this is the prof's transcript
    text_content = re.sub(r"\(.*\)", "", str(text_content))
    nlp = English()  # just the language with no pipeline
    nlp.add_pipe("sentencizer")
    doc = nlp(text_content)
    transcript = []
    for sentence in doc.sents:
        transcript.append(sentence.text.strip())
    return transcript


def get_title_from_chapters(chapter: Tuple[str]) -> str:
    """Returns the title of the chapters."""
    title = chapter[0].split(".")[0]
    return title


# options for ANN "angular", "euclidean", "manhattan", "hamming", or "dot"
def get_similar_sentences(prof_transcript, prof_embeddings, headlines, n=3):
    """Returns the top n similar sentences to each headline."""
    assert len(prof_embeddings) == len(prof_transcript)
    phrases_to_vectors = {}
    for sentence in prof_transcript:
        phrases_to_vectors[sentence] = prof_embeddings[0]  # map our phrases to embeddings

    seen = set()  # seen phrases, prevent duplicate similar sentences
    similar_sentences = {}  # key: headline, value: (headline embedding, list of top 3 phrases, list of embeddings)

    search_index = annoy.AnnoyIndex(
        len(prof_embeddings[0]), "angular"
    )  # build ANN search tree
    for i in range(len(prof_embeddings)):
        search_index.add_item(i, prof_embeddings[i])
    search_index.build(10)  # 10 trees

    for headline in headlines:
        headline_embedding = co.embed(
            texts=[headline], model="large", truncate="RIGHT"
        ).embeddings
        similar_sentences[headline] = (headline_embedding[0], [], [])

    for headline in headlines:
        top = search_index.get_nns_by_vector(similar_sentences[headline][0], n * 2)
        for i in top:
            if prof_transcript[i] in seen:
                continue
            seen.add(prof_transcript[i])
            similar_sentences[headline][1].append(prof_transcript[i])
            similar_sentences[headline][2].append(prof_embeddings[i])

    return similar_sentences


def summarize(text):
    """Returns a summary of the text."""
    prompt = f'''
        "The killer whale or orca (Orcinus orca) is a toothed whale
        belonging to the oceanic dolphin family, of which it is the largest member"
        In summary: "The killer whale or orca is the largest type of dolphin"

        "Cognitive Science is the interdisciplinary, scientific study of the mind and its processes.
        It examines the nature, the tasks, and the functions of cognition."
        In summary: "Cognitive Science: the study of the mind and its processes"

        "{text}"
        In summary:"'''

    prediction = co.generate(
        model='large',
        prompt=prompt,
        return_likelihoods = 'GENERATION',
        stop_sequences=['"'],
        max_tokens=55,
        temperature=0.75,
        num_generations=1,
        k=0,
        p=0.85
    ).generations[0].text
    return prediction
    

def get_flashcards(url):
    """Returns a set of flashcards for the given url."""
    # get the transcript and relevant data
    prof_data = get_prof_data(url)  # (transcript, embeddings, entities, chapters)
    prof_transcript = prof_data[0]  # list[str]
    prof_embeddings = prof_data[1]
    entities = prof_data[2]
    chapters = prof_data[3]
    titles = [get_title_from_chapters(c) for c in chapters]
    headlines = [c[1] for c in chapters]
    similar_sentences = get_similar_sentences(
        prof_transcript, prof_embeddings, headlines
    )
    # ^^^ key: headline, value: (headline embedding, list of top 3 phrases, list of embeddings)
    flashcards = []
    for t, h, c in zip(titles, headlines, chapters):
        sents = " ".join(similar_sentences[h][1])
        back = f"{h} {sents}"
        embedding = co.embed(texts=[back], model="large", truncate="RIGHT").embeddings[0]
        # if back is too long, summarize it with cohere
        if len(back) > 150:
            back = summarize(back)
        flashcards.append(
            Flashcard(
                t,
                back,
                None,
                None,
                h,
                similar_sentences[h][0],
                embedding,
                None
            )
        )

    return flashcards
