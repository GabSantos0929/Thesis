import whisper
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Load Whisper model (can be 'tiny', 'base', 'small', 'medium', 'large')
model = whisper.load_model("base")

# Transcribe audio
def transcribe_audio(audio_path):
    print("Transcribing with Whisper...")
    result = model.transcribe(audio_path)
    print("Detected Language:", result["language"])
    return result["text"]

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
    audio_path = "audio_files/sample_audio6.mp3"  # replace with your audio file
    transcript = transcribe_audio(audio_path)
    print("Transcript:", transcript)

    gpt_response = process_with_gpt(transcript)
    print("GPT Response:", gpt_response)
