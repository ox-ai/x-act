from faster_whisper import WhisperModel

from xact.config.gen import config
from xact.log.config import log_manager

log = log_manager.init(__name__)


class VoiceModel:
    def __init__(self,model=config.XACT_WHISPER_MODEL,device="cpu",compute_type="int8"):
        self.model = WhisperModel(model,device=device,compute_type=compute_type) 


    def transcribe(self,audio):
        segments, info = self.model.transcribe(audio=audio,beam_size=5)
        prompts = []
        for segment in segments:
            prompts.append(segment.text)
            transcribed = ("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            log.info(transcribed)

        prompt = "".join(prompts)
        return prompt