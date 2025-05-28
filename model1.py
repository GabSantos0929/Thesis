import whisper
import openai
import os

# Load Whisper model (can be 'tiny', 'base', 'small', 'medium', 'large')
model = whisper.load_model("base")

# Transcribe audio
def transcribe_audio(audio_path):
    print("Transcribing with Whisper...")
    result = model.transcribe(audio_path)
    return result["text"]

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
    audio_path = "audio_files/sample_audio3.wav"  # replace with your audio file
    transcript = transcribe_audio(audio_path)
    print("Transcript:", transcript)

    gpt_response = process_with_gpt(transcript)
    print("GPT Response:", gpt_response)
