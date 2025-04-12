from dotenv import load_dotenv
import os
import requests
import time
import json
from pathlib import Path

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def upload_audio(filepath):
    with open(filepath, "rb") as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers={'authorization': ASSEMBLYAI_API_KEY},
            files={'file': f}
        )
    
    return response.json()['upload_url']


def start_transcription(audio_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json_data = {
        "audio_url": audio_url,
        "auto_chapters": False,
        "speaker_labels": True
    }

    response = requests.post(
        endpoint,
        json=json_data,
        headers={"authorization": ASSEMBLYAI_API_KEY}
    )
    return response.json()["id"]

def poll_transcription(transcript_id):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    while True:
        response = requests.get(endpoint, headers={"authorization": ASSEMBLYAI_API_KEY})
        status = response.json()["status"]
        if status == "completed":
            return response.json()
        elif status == "error":
            raise Exception(f"Transcription failed: {response.json()['error']}")
        print("Waiting for transcription...")
        time.sleep(3)

def save_transcript_as_messages(transcript_json, output_path="data/transcripts.json"):
    results = []
    for utterance in transcript_json.get("utterances", []):
        results.append({
            "user": utterance["speaker"],
            "text": utterance["text"],
            "timestamp": transcript_json["created"],
            "meeting_id": transcript_json["id"]
        })

    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Transcript saved to {output_path} ({len(results)} messages)")


def main(audio_filepath):
    audio_url = upload_audio(audio_filepath)
    transcript_id = start_transcription(audio_url)
    transcript_json = poll_transcription(transcript_id)
    save_transcript_as_messages(transcript_json)
    
