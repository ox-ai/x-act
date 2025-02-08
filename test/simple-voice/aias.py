import time
import pyttsx3
from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import VoiceModel
from xact.speech_gen.echo import play_audio
from xact.llm.llm import LLM

model="qwen2.5:1.5b "
llm = LLM(model)
vmd = VoiceModel()
engine = pyttsx3.init()


def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()
# Function to handle the continuous listening and transcription loop
def listen_and_transcribe(mic):
    try:
        # Continuously listen for speech
        while True:
            print("Listening for speech...")
            mic.start_recording()
            

            # Wait for audio data to be available
            time.sleep(5)
            audio_data = mic.get_audio_data()
            mic.stop_recording()
            print("processing")
            
            if audio_data:
                # Save the audio data to a temporary file
                temp_file = mic.save_audio_to_tempfile_np(audio_data)
                
                if temp_file:
                    # Transcribe the audio using the transcribe function
                    transcribed_text = vmd.transcribe(temp_file)
                    print(f"you : {transcribed_text}")
                    transcribed_text+" give the answr short"
                    res = llm.generate(transcribed_text,model)
                    speak(res)
                    print(f"ai  : {res}")
                else:
                    print("Failed to save audio data.")
            
            # Stop recording for the current loop and wait before listening again
            
             # Small delay to prevent continuous rapid calls
    except KeyboardInterrupt:
        # Handle stopping the loop gracefully
        print("Stopped listening.")
        mic.stop_recording()
        mic.close()

# Create microphone instance and start the listening loop
mic = Microphone()
listen_and_transcribe(mic)
