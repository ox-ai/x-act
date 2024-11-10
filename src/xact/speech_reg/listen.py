import tempfile
import wave
import numpy as np
import soundfile as sf
import pyaudio
import queue

from xact.settings import config
from xact.utils.log import logger



class Microphone:
    """
    system microphone api access manager
    """
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=config.AUDIO_FORMAT,
            channels=config.AUDIO_CHANNELS,
            rate=config.AUDIO_RATE,
            input=True,
            frames_per_buffer=config.AUDIO_CHUNK,
            stream_callback=self.callback,
        )
        self.queue = queue.Queue()
        self.is_recording = False
        self.is_receiving = False
        logger.info("Microphone init")

    def callback(self, in_data, frame_count, time_info, status):
        if self.is_recording and not self.is_receiving:
            self.queue.put(in_data)
        return (None, pyaudio.paContinue)

    def start_recording(self):
        self.is_recording = True
        logger.info("Started recording")

    def stop_recording(self):
        self.is_recording = False
        logger.info("Stopped recording")

    def start_receiving(self):
        self.is_receiving = True
        self.is_recording = False
        logger.info("Started receiving")

    def stop_receiving(self):
        self.is_receiving = False
        logger.info("Stopped receiving")

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        logger.info("Microphone closed")

    def get_audio_data(self):
        data = b""
        while not self.queue.empty():
            data += self.queue.get()
        return data if data else None

    def save_audio_to_tempfile(self, audio_data):
        # Save the audio data to a temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        with wave.open(temp_file, 'wb') as wf:
            wf.setnchannels(config.AUDIO_CHANNELS)
            wf.setsampwidth(self.p.get_sample_size(config.AUDIO_FORMAT))
            wf.setframerate(config.AUDIO_RATE)
            wf.writeframes(audio_data)
        return temp_file.name


    def save_audio_to_tempfile_np(audio_data):
        # Create a temporary file to store audio data
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            # Write audio data to the temp file
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            sf.write(temp_file, audio_array, config.AUDIO_RATE)
            return temp_file.name
    