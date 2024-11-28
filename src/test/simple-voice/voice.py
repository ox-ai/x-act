
print("init")


import pyttsx3
import time

from xact.speech_reg.listen import Microphone
from xact.speech_reg.whisper import transcribe
print("f")
from xact.speech_gen.echo import play_audio
from xact.llm.openai_client import llm_client
from xact.utils.log import logger

print("f")
mic = Microphone()

model_size = "small"

# # Run on GPU with FP16
# whisper_model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8

model = "qwen2.5:1.5b "


# Initialize Text-to-Speech engine (for speaking the response)
engine = pyttsx3.init()



# Function to generate a response using OpenAI API
def generate_response(prompt):
    print("Generating response...")
    try:
        # Send the transcribed text to OpenAI's GPT model
        chat_completion = llm_client.chat.completions.create(
                    messages=[
                        {
                            "role":"system",
                            "content":"your a contract document analyst based on the given topic and use the documents give the detiled list of data",
                        },
                        {
                            "role": "user",
                            "content": prompt.strip(),
                        }
                    ],
                    model=model,
                    temperature=0,
                )
                
        return chat_completion.choices[0].message.content
            
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Function to speak the generated response using Text-to-Speech
def speak(text):
    print(f"Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

# Main assistant loop
def main():
    while True:
        try:
            # Step 1: Listen for user's command
            print("lisning ...")
            mic.start_recording()
            mic.start_receiving()
            time.sleep(5)
            mic.stop_receiving()
            mic.stop_recording()
            audio_data = mic.get_audio_data()
            path = mic.save_audio_to_tempfile_np(audio_data)
            if not path:
                continue
            user_input = transcribe(path)
            print(f"You said: {user_input}")
            
            # Step 2: Generate a response from OpenAI based on the user's input
            if not user_input:
                continue
            response = generate_response(user_input)
            
            # Step 3: Speak the response aloud
            speak(response)
        
        except KeyboardInterrupt:
            mic.stop_recording()
            print("Assistant terminated.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(2)  # Delay before next attempt

# Run the assistant
if __name__ == "__main__":
    main()
