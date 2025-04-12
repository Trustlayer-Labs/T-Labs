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
    print(audio_url)
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
    # Safely get the timestamp, defaulting to None if 'created' key is absent
    creation_timestamp = transcript_json.get("created")
    
    # Add the full transcript as a single entry
    full_transcript = transcript_json.get("text", "")
    if full_transcript:
        results.append({
            "user": "Full Transcript",
            "text": full_transcript,
            "timestamp": creation_timestamp,
            "meeting_id": transcript_json["id"]
        })
    
    # Process individual utterances if available
    for utterance in transcript_json.get("utterances", []):
        results.append({
            "user": utterance["speaker"],
            "text": utterance["text"],
            "timestamp": creation_timestamp,
            "meeting_id": transcript_json["id"]
        })

    # Save the results to the specified output path
    Path(output_path).parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Transcript saved to {output_path} ({len(results)} messages)")


def main(audio_filepath):
    #audio_url = upload_audio(audio_filepath)
    audio_url = "https://assembly.ai/sports_injuries.mp3"
    transcript_id = start_transcription(audio_url)
    transcript_json = poll_transcription(transcript_id)
    print(transcript_json)
    save_transcript_as_messages(transcript_json)


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent  # T-Labs directory
    audio_filepath = root_dir / "data" / "audio" / "156550__acclivity__a-dream-within-a-dream.wav" 
    print("test", audio_filepath)
    main(audio_filepath)


