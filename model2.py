import os
import openai
from pocketsphinx import AudioFile

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
def process_with_gpt(prompt, model_name="gpt-3.5-turbo"):
    print("Sending to GPT...")
    client = openai.OpenAI(api_key=os.getenv("API_KEY"))
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an assistant helping with voice-based inputs."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    audio_path = "audio_files/sample_audio3.wav"  # PocketSphinx works best with WAV files (mono, 16kHz)
    transcript = transcribe_audio(audio_path)
    gpt_response = process_with_gpt(transcript)
    print("GPT Response:", gpt_response)
