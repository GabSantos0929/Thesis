import whisper

# Load Whisper model (can be 'tiny', 'base', 'small', 'medium', 'large')
model = whisper.load_model("base")

# Transcribe audio
def transcribe_audio(audio_path):
    print("Transcribing with Whisper...")
    result = model.transcribe(audio_path)
    print("Detected Language:", result["language"])
    return result["text"]
