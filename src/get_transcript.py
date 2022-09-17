from load_audio import get_response, get_response_from_url

filename = "Asking Harvard Students If They Ever Sleep.mp3"


def get_transcript_from_url(url):
    response_json = get_response_from_url(url)
    speakers = response_json['utterances']

    speaker_to_str = {'speaker_lst': []}
    for d in speakers:   # speaker, text
        speaker = d['speaker']
        if speaker not in speaker_to_str:
            speaker_to_str['speaker_lst'].append(speaker)

            if speaker == 'A':
                speaker_to_str[speaker] = d['text']
            else:
                speaker_to_str[speaker] = [d['text']]
                speaker_to_str['A'] += f'(speaker: {d["speaker"]})'
        else:
            if speaker == 'A':
                speaker_to_str[speaker] += ('\n' + d['text'])
            else:
                speaker_to_str[speaker].append(d['text'])
                speaker_to_str['A'] += f'(speaker: {d["speaker"]})'

    speaker_to_str['chapters'] = []
    for chapter in response_json['chapters']:
        speaker_to_str['chapters'].append((chapter['gist'], chapter['headline'], chapter['summary']))

    speaker_to_str['entities'] = set()
    for entity in response_json['entities']:
        if entity['entity_type'] in {'person_name', 'location', 'email_address', 'date', 'event', 'religion',
                                     'political_affiliation'}:
            speaker_to_str['entities'].add(entity['text'])

    print(speaker_to_str)
    return speaker_to_str


def get_transcript(file):
    # assumption: speaker A is the prof <3
    response_json = get_response(filename)
    speakers = response_json["utterances"]

    speaker_to_str = {"speaker_lst": []}
    for d in speakers:  # speaker, text
        speaker = d["speaker"]
        if speaker not in speaker_to_str:
            speaker_to_str["speaker_lst"].append(speaker)

            if speaker == "A":
                speaker_to_str[speaker] = d["text"]
            else:
                speaker_to_str[speaker] = [
                    d["text"]
                ]  # non-prof speakers get a list of questions/comments
                speaker_to_str[
                    "A"
                ] += f'(speaker: {d["speaker"]})'  # marking who's Q it was
        else:
            if speaker == "A":
                speaker_to_str[speaker] += "\n" + d["text"]
            else:
                speaker_to_str[speaker].append(d["text"])
                speaker_to_str[
                    "A"
                ] += f'(speaker: {d["speaker"]})'  # marking who's Q it was

    speaker_to_str["chapters"] = []
    for chapter in response_json["chapters"]:
        speaker_to_str["chapters"].append(
            (chapter["gist"], chapter["headline"], chapter["summary"])
        )

    speaker_to_str['entities'] = set()
    for entity in response_json['entities']:
        if entity['entity_type'] in {'person_name', 'location', 'email_address', 'date', 'event', 'religion',
                                     'political_affiliation'}:
            speaker_to_str['entities'].add(entity['text'])

    return speaker_to_str
