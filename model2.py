import os
import requests
from pocketsphinx import AudioFile
from dotenv import load_dotenv
load_dotenv()

# Transcribe audio using PocketSphinx
def transcribe_audio(audio_path):
    print("Transcribing with PocketSphinx...")

    # Set up configuration for decoder
    config = {
        'verbose': False,
        'audio_file': audio_path
    }

    audio = AudioFile(**config)
    transcript = ""

    for phrase in audio:
        transcript += phrase.hypothesis() + " "

    print("Transcript:", transcript.strip())
    return transcript.strip()

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
            {"role": "system", "content": "You are an assistant helping with voice-based inputs."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)
        return "Error contacting GPT"

# Example usage
if __name__ == "__main__":
    audio_path = "audio_files/sample_audio3.wav"  # PocketSphinx works best with WAV files (mono, 16kHz)
    transcript = transcribe_audio(audio_path)
    gpt_response = process_with_gpt(transcript)
    print("GPT Response:", gpt_response)
