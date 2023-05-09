from pydub import AudioSegment
from pydub.playback import play

def play_audio_file(file_path):
    audio = AudioSegment.from_wav(file_path)
    play(audio)