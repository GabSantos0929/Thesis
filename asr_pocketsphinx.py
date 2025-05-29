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

    transcript = transcript.strip()
    print("Transcript:", transcript)
    return transcript
