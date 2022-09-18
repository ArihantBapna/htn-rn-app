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
    headers = {'authorization': "c4187da13e3d4c6fa7ead1cac4246a1f", 'content-type': "application/json"}
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
