import time
import sys
from xact.utils.log import logger



from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import transcribe


class SpeechToText:
    def __init__(self):
        self.mic = Microphone()



    def listen_and_transcribe(self):
        try:
            logger.info("Listening for sound... Press Ctrl+C to stop.")
            self.mic.start_recording()

            while True:
                # Listen for audio
                audio_data = self.mic.get_audio_data()

                if audio_data:
                    logger.info("Sound detected, transcribing...")
                    # Save audio to a temporary file and transcribe
                    temp_audio_file = self.mic.save_audio_to_tempfile(audio_data)
                    text = transcribe(temp_audio_file)
                    logger.info(f"Transcribed Text: {text}")
                else:
                    logger.info("No sound detected, still listening...")

                time.sleep(0.5)  # Sleep to avoid busy-waiting and CPU overload
        except KeyboardInterrupt:
            logger.info("\nTerminating. Stopping mic...")
            self.mic.stop_recording()
            self.mic.close()
            sys.exit(0)

def main():
    speech_to_text = SpeechToText()
    speech_to_text.listen_and_transcribe()

if __name__ == "__main__":
    main()

