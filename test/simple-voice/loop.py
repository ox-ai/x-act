import time
from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import transcribe

# Function to handle the continuous listening and transcription loop
def listen_and_transcribe(mic):
    try:
        # Continuously listen for speech
        while True:
            print("Listening for speech...")
            mic.start_recording()
            print("processing")

            # Wait for audio data to be available
            time.sleep(5)
            audio_data = mic.get_audio_data()
            mic.stop_recording()
            
            if audio_data:
                # Save the audio data to a temporary file
                temp_file = mic.save_audio_to_tempfile_np(audio_data)
                
                if temp_file:
                    # Transcribe the audio using the transcribe function
                    transcribed_text = transcribe(temp_file)
                    print(f"Transcription: {transcribed_text}")
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
