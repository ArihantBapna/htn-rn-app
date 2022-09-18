import requests

filename = "Asking Harvard Students If They Ever Sleep.mp3"


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data


def get_response_from_url(url):
    headers = {'authorization': "b479f0aa918d4566aaacdec3f82c9b54", 'content-type': "application/json"}
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": url,
        "disfluencies": True,
        "speaker_labels": True,
        "auto_chapters": True,
        "entity_detection": True,
    }
    response = requests.post(endpoint, json=json, headers=headers)
    transcript_id = response.json()['id']
    print(transcript_id)
    curr_status = response.json()['status']
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while curr_status != 'completed' and curr_status != 'error' or curr_status == 'queued':
        response = requests.get(endpoint, headers=headers)
        curr_status = response.json()['status']

    if curr_status == 'error':
        return {"error": "error"}
    return response.json()


def get_response(file):
    headers = {'authorization': "b479f0aa918d4566aaacdec3f82c9b54"}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(file))
    res = response.json()  # upload audio
    if res['upload_url']:
        endpoint = "https://api.assemblyai.com/v2/transcript"
        headers['content-type'] = "application/json"
        print(headers)
        json = {
            "audio_url": res['upload_url'],
            "disfluencies": True,  # TODO: test on audio file that contains filler
            "speaker_labels": True,  # TODO: test on audio file that (a) has multiple speakers one after the other;
                                    # TODO: (b) overlapping speakers
            "auto_chapters": True,   # TODO: test
            "entity_detection": True,  # TODO: test
        }
        response = requests.post(endpoint, json=json, headers=headers)
        print(response.json())  # begin transcript process

        transcript_id = response.json()['id']  # get reqs until success
        curr_status = response.json()['status']
        endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        headers = {
            "authorization": "b479f0aa918d4566aaacdec3f82c9b54",
        }
        while curr_status != 'completed' and curr_status != 'error':
            response = requests.get(endpoint, headers=headers)
            curr_status = response.json()['status']
            print(curr_status)

        if curr_status == 'error':
            print("you suck")
            return
        return response.json()
    return "you also suck"
