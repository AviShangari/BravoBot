import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import time
import queue
import warnings
import re
from pynput import keyboard

warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")

class SpeechInterface:
    def __init__(self):
        self.model = whisper.load_model("small")
        self.logger = None
        device = str(self.model.device)
        if "cuda" in device:
            device = "gpu"
        elif "cpu" in device:
            device = "cpu"
        print("System Configuration:\nBravoBot is using:", device)
        print("---------------------------------------")

        self.engine = pyttsx3.init()
        self.stop_requested = True
        self.skip_next_input = False
        self._stop_listener_thread_started = False

    def _record_audio(self):
        samplerate = 16000
        silence_threshold = 0.01  # RMS threshold
        silence_duration = 2.0
        max_record_duration = 45.0  # safety cap
        blocksize = 1024
        silence_blocks = int(samplerate * silence_duration / blocksize)

        print("Recording... Speak now")
        q = queue.Queue()
        rec = []
        silent_count = 0
        speaking_started = False
        start_time = time.time()

        def callback(indata, frames, time_info, status):
            q.put(indata.copy())

        with sd.InputStream(samplerate=samplerate, channels=1, callback=callback, blocksize=blocksize):
            while True:
                data = q.get()
                rec.append(data)
                rms = np.sqrt(np.mean(data**2))

                if rms > silence_threshold:
                    speaking_started = True
                    silent_count = 0
                elif speaking_started:
                    silent_count += 1

                if speaking_started and silent_count > silence_blocks:
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
        cleaned_text = re.sub(r'[\'"*`\\#~]', '', text)
        self.stop_requested = False

        parts = re.split(r'(?<=[.!?])\s+', cleaned_text)
        for part in parts:
            if self.stop_requested:
                break
            self.engine.say(part)
            self.engine.runAndWait()

    def stop_speaking(self):
        self.stop_requested = True
        self.engine.stop()
        # self.engine = pyttsx3.init()
        self.skip_next_input = True

    def listen_for_keyboard_stop(self):
        if self._stop_listener_thread_started:
            return

        def on_activate():
            print("Speech interrupted via Shift + Q.")
            self.stop_requested = True

        listener = keyboard.GlobalHotKeys({'<shift>+q': on_activate})
        listener.daemon = True
        listener.start()
        self._stop_listener_thread_started = True
    
    def speak_and_log(self, text):
        self.speak(text)
        self.logger.log("bot", text)
