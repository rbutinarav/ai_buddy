from audio_functions import audio_recorder_st, wave_to_text, detect_language

#open and load the audio file
audio_wave = "test.wav"

result = wave_to_text(audio_wave, language="it-IT")
print(result)
