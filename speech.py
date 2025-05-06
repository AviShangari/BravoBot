import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time
import queue

class SpeechInterface:
    def __init__(self):
        self.model = whisper.load_model("small")
        print("Whisper is using:", self.model.device)
        self.engine = pyttsx3.init()

    def _record_audio(self):
        samplerate = 16000
        silence_threshold = 300
        silence_duration = 4.0
        min_record_duration = 2.0
        blocksize = 1024
        silence_blocks = int(samplerate * silence_duration / blocksize)

        print("Recording... Speak now")
        q = queue.Queue()
        rec = []
        start_time = time.time()

        def callback(indata, frames, time_info, status):
            q.put(indata.copy())

        with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, blocksize=blocksize):
            silent_count = 0
            while True:
                data = q.get()
                rec.append(data)
                volume = np.linalg.norm(data)

                if volume < silence_threshold:
                    silent_count += 1
                else:
                    silent_count = 0

                if silent_count > silence_blocks and (time.time() - start_time) > min_record_duration:
                    break

        audio = np.concatenate(rec, axis=0)
        return samplerate, audio.flatten()

    def _transcribe(self, samplerate, audio):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
            wav.write(f.name, samplerate, audio)
            result = self.model.transcribe(f.name)
        return result["text"].lower().strip()

    def listen(self):
        samplerate, audio = self._record_audio()
        return self._transcribe(samplerate, audio)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
