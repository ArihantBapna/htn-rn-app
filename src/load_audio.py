import requests
import os
from dotenv import load_dotenv

load_dotenv()
assembly_api = os.getenv('assembly')


def get_response_from_url(url):
    headers = {'authorization': assembly_api, 'content-type': "application/json"}
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
