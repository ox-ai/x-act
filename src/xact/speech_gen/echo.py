
import asyncio
import pyaudio


from xact.settings import config
from xact.utils.log import logger


async def play_audio(audio_data):
    p = pyaudio.PyAudio()
    stream = p.open(format=config.AUDIO_FORMAT, channels=config.AUDIO_CHANNELS, rate=config.AUDIO_RATE, output=True)
    stream.write(audio_data)

    # Add a small delay of silence at the end to prevent popping, and weird cuts off sounds
    silence_duration = 0.4
    silence_frames = int(config.AUDIO_RATE * silence_duration)
    silence = b"\x00" * (
        silence_frames * config.AUDIO_CHANNELS * 2
    )  # 2 bytes per sample for 16-bit audio
    stream.write(silence)

    # Add a small pause before closing the stream to make sure the audio is fully played
    await asyncio.sleep(0.5)

    stream.stop_stream()
    stream.close()
    p.terminate()
    logger.debug("Audio playback completed")
