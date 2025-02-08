import time

# Assuming the Microphone class is imported from your module
from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import transcribe
# Create an instance of the Microphone class
mic = Microphone()

# Start recording
mic.start_recording()
print("Recording...")

# Record for a few seconds
time.sleep(5)  # Sleep for 5 seconds to simulate recording

# Stop recording
mic.stop_recording()
print("Stopped recording.")

# Retrieve the audio data
audio_data = mic.get_audio_data()

# Check if there is audio data and save it
if audio_data:
    print("Saving audio data to temporary file...")
    temp_file = mic.save_audio_to_tempfile_np(audio_data)
    print(f"Audio saved to: {temp_file}")
    user_input = transcribe(temp_file)
    print(f"You said: {user_input}")
else:
    print("No audio data available.")

# Close the microphone stream
mic.close()
