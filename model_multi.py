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
    api_key = os.getenv("OPENROUTER_API_KEY")  # Make sure to set this in your environment

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": conversation_history
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return reply
    else:
        print("Error:", response.status_code, response.text)
        return None

def build_google_maps_url(gpt_response):
    origin = gpt_response.get("origin", "current location")
    destination = gpt_response["destination"]
    via = gpt_response.get("via", "")
    travel_mode = "driving"

    # Let Google Maps handle location detection if origin is "current location"
    if origin.lower() == "<optional>":
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

    waypoints = ""
    if via:
        waypoint_list = [place.strip() for place in via.split(",")]
        waypoints = "|".join(waypoint_list)
    if waypoints:
        params["waypoints"] = waypoints

    # Encode parameters
    url = base_url + "&" + urllib.parse.urlencode(params)
    return url

def is_json(text):
    try:
        json.loads(text)
        return True
    except:
        return False

if __name__ == "__main__":
    audio_path = "audio_files/sample_audio7.wav"  # replace with your audio file
    transcript = vosk_transcribe(audio_path)
    # transcript = "Can you take me to the airport using Skyway?" # enter your navigation prompts here
    print("Transcript:", transcript)

    conversation_history = [
        {"role": "system", "content": "You are a voice-based navigation assistant. Your goal is to extract and clarify travel intent. At the end, respond ONLY with this JSON: {\"origin\": \"<optional>\", \"destination\": \"<required>\", \"via\": \"<optional>\", \"preference\": \"<optional>\"}."},
        {"role": "user", "content": transcript}
    ]

    while True:
        response = process_with_gpt(conversation_history)
        if not response:
            break

        print("AI:", response)
        if is_json(response):
            gpt_response = json.loads(response)
            map_url = build_google_maps_url(gpt_response)
            print("Google Maps URL:", map_url)
            break

        user_reply = input("You: ")
        conversation_history.append({"role": "assistant", "content": response})
        conversation_history.append({"role": "user", "content": user_reply})
