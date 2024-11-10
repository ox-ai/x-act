from faster_whisper import WhisperModel

from xact.settings import config
from xact.utils.log import logger

model = WhisperModel(config.XACT_WHISPER_MODEL)


def transcribe(audio):
    segments, info = model.transcribe(audio=audio)
    prompts = []
    for segment in segments:
        prompts.append(segment.text)
        transcribed = ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        print(transcribed)
        logger.info(transcribed)

    prompt = "".join(prompts)
    return prompt