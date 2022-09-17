from load_audio import get_response

filename = "Asking Harvard Students If They Ever Sleep.mp3"

def generate_prof_transcript(file):
    # assumption: speaker A is the prof <3
    response_json = get_response(file)
    speakers = response_json['utterances']

    speaker_to_str = {}
    for d in speakers:   # speaker, text
        speaker = d['speaker']
        if speaker not in speaker_to_str:
            if speaker == 'A':
                speaker_to_str[speaker] = d['text']
            else:
                speaker_to_str[speaker] = [d['text']]  # non-prof speakers get a list of questions/comments
                speaker_to_str['A'] += f'(speaker: {d["speaker"]})'  # marking who's Q it was
        else:
            if speaker == 'A':
                speaker_to_str[speaker] += ('\n' + d['text'])
            else:
                speaker_to_str[speaker].append(d['text'])
                speaker_to_str['A'] += f'(speaker: {d["speaker"]})'  # marking who's Q it was
    print(speaker_to_str)
    return speaker_to_str


