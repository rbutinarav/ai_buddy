from pydub import AudioSegment
from pydub.playback import play
from playsound import playsound

def play_audio_file_pydub(file_path):
#not working for missing libraries
    audio = AudioSegment.from_wav(file_path)
    play(audio)

from playsound import playsound

def play_audio_file(file_path):
    playsound(file_path)


play_audio_file("audio_files/audio_file_2023-05-09-11-06-22.wav")