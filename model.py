import requests
import os
import json
import urllib.parse
from asr_whisper import transcribe_audio as whisper_transcribe
from asr_pocketsphinx import transcribe_audio as pocketsphinx_transcribe
from dotenv import load_dotenv
load_dotenv()

# Send transcription to GPT
def process_with_gpt(prompt, model_name="openai/gpt-3.5-turbo"):
    print("Sending to GPT via OpenRouter...")
    api_key = os.getenv("OPENROUTER_API_KEY")  # Make sure to set this in your environment

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a voice-based navigation assistant. Given a user's spoken request, extract the origin (if any), destination, and preferred route (e.g., 'via EDSA'). Respond in this JSON format: {\"origin\": \"<optional>\", \"destination\": \"<required>\", \"via\": \"<optional>\"}."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)
        return "Error contacting GPT"

def build_google_maps_url(gpt_response):
    origin = gpt_response.get("origin", "current location")
    destination = gpt_response["destination"]
    via = gpt_response.get("via", "")
    travel_mode = "driving"

    # Let Google Maps handle location detection if origin is "current location"
    if origin.lower() == "current location":
        origin = "current+location"

    # URL construction
    base_url = "https://www.google.com/maps/dir/?api=1"
    params = {
        "origin": origin,
        "destination": destination,
        "travelmode": travel_mode,
        "avoid": "tolls",
        "dir_action": "navigate"
    }

    if via:
        params["waypoints"] = via

    # Encode parameters
    url = base_url + "&" + urllib.parse.urlencode(params)
    return url

# Example usage
if __name__ == "__main__":
    audio_path = "audio_files/sample_audio2.wav"  # replace with your audio file
    # transcript = whisper_transcribe(audio_path)
    transcript = "Go to MOA using Skyway. Assuming I'm at DLSU right now."
    print("Transcript:", transcript)

    gpt_response = process_with_gpt(transcript)
    print("GPT Response:", gpt_response)

    try:
        gpt_response = json.loads(gpt_response)
        map_url = build_google_maps_url(gpt_response)
        print("Google Maps URL:", map_url)
    except json.JSONDecodeError:
        print("Invalid JSON from GPT:", gpt_response)
