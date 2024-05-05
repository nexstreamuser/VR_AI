from vosk import Model, KaldiRecognizer
import pyaudio
import json

RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1
INPUT = True
FRAMES_PER_BUFFER = 4096
CHUNK_SIZE = 4096

stt_model = Model("models/vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(stt_model, RATE)

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=INPUT, frames_per_buffer=FRAMES_PER_BUFFER)
stream.start_stream()

while True:
    data = stream.read(CHUNK_SIZE)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        text = json.loads(text)
        print(text["text"])