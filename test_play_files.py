from pydub import AudioSegment
from pydub.playback import play

def play_audio_file(file_path):
    audio = AudioSegment.from_wav(file_path)
    play(audio)


play_audio_file("audio_files/audio_file_2023-05-09-11-06-22.wav")