import time
import keyboard  # For detecting key presses
import pyttsx3
from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import VoiceModel
from xact.speech_gen.echo import play_audio
from xact.llm.llm import LLM

model="qwen2.5:1.5b"
llm = LLM(model)
vmd = VoiceModel()


engine = pyttsx3.init()


def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

custom_shortcut_key = "alt+x"
# Function to handle listening and transcription when a key is pressed
def listen_and_transcribe(mic):
    try:
        print("Press ctrl+alt+x to start/stop recording and 'q' to quit.")
        i=0
        while True:
            i=i+1
            print(f"\rProcessing {i}% complete", end='', flush=True)
            # Wait for the custom_shortcut_key key to start or stop recording
            if keyboard.is_pressed(custom_shortcut_key):  # Detect the custom_shortcut_key key press
                print("custom_shortcut_keykey pressed - Start/Stop recording.")
                mic.start_recording()

                # Wait for a short period while the recording happens
                print("Recording... (Press custom_shortcut_key again to stop recording)")

                # Let the user record until they press custom_shortcut_key again
                while keyboard.is_pressed(custom_shortcut_key):
                    time.sleep(0.1)  # Check if the key is still being pressed
                 
                mic.stop_recording()  # Stop recording when the key is released
                print("Stopped recording.")

                # Retrieve the audio data after stopping the recording
                audio_data = mic.get_audio_data()
                
                if audio_data:
                    # Save the audio data to a temporary file
                    temp_file = mic.save_audio_to_tempfile_np(audio_data)
                    
                    if temp_file:
                        # Transcribe the audio using the transcribe function
                        transcribed_text = vmd.transcribe(temp_file)
                        print(f"you : {transcribed_text}")
                        transcribed_text+" give the answer short just less then 200 words and give just text output dont give in markdown format"
                        res = llm.generate(transcribed_text,model)
                        speak(res)
                        print(f"ai  : {res}")
                    else:
                        print("Failed to save audio data.")
                else:
                    print("No audio data available.")
                
                # Add a small delay to avoid rapid consecutive detections
                time.sleep(1)

            # Check if the user presses 'q' to quit the loop
            if keyboard.is_pressed('q'):
                print("Quitting...")
                break
            
            time.sleep(0.1)  # Prevent tight looping when idle

    except KeyboardInterrupt:
        # Handle stopping the loop gracefully
        print("Stopped listening.")
        mic.stop_recording()
        mic.close()

# Create microphone instance and start the listening loop
mic = Microphone()
listen_and_transcribe(mic)
