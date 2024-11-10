import os
import json
from pathlib import Path
import pyaudio
from xact.utils.log import logger

# Paths for configuration storage
MASTER_BASE = ".ox-ai"
XACT_BASE = "xact"
XACT_DB = "db"
XACT_DOC = "doc"
XACT_VEC_DB = "vec_db"
XACT_BASE_Path = Path.home() / MASTER_BASE / XACT_BASE 
XACT_DB_Path = XACT_BASE_Path / XACT_DB
XACT_DOC_Path = XACT_BASE_Path / XACT_DOC
XACT_VEC_DB_Path = XACT_BASE_Path / XACT_VEC_DB


class SingletonMeta(type):
    """A thread-safe Singleton base class."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Settings(metaclass=SingletonMeta):
    """Central settings class to load and save configuration as JSON."""
    def __init__(self, config_file="settings.json"):
        self.config_file = XACT_BASE_Path / config_file
        self.config_data = {}
        self.load()

    def load(self):
        """Load configuration from a JSON file, if available."""
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                self.config_data.update(json.load(f))
        logger.info("Settings loaded from JSON.")

    def save(self, filename="settings_updated.json"):
        """Save the current configuration to a JSON file."""
        save_path = XACT_BASE_Path / filename
        # Ensure the directory exists
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, "w") as f:
            json.dump(self.config_data, f, indent=4)
        logger.info("Settings saved to JSON.")


    def get(self, key, default=None):
        """Get a configuration value by key, with optional default."""
      
        data = self.config_data
        
        data = data.get(key, default)
        if data is default:
            self.set(key,data)
        return data

    def set(self, key, value):
        """Set a configuration value by key."""

        self.config_data[key]=str(value)
    


class Config:
    def __init__(self, settings: Settings):
        self.XACT_LLM_BASE_URL = settings.get("XACT_LLM_BASE_URL","http://localhost:11434/v1/")
        self.XACT_LLM_API_KEY = settings.get("XACT_LLM_API_KEY","ollama")
        self.XACT_LLM_MODEL = settings.get("XACT_LLM_MODEL","qwen2.5-coder:1.5b")
        self.XACT_LLM_EMBEDDING_MODEL = settings.get("XACT_LLM_EMBEDDING_MODEL","nomic-embed-text")
        self.XACT_WHISPER_BASE_URL = settings.get("XACT_WHISPER_BASE_URL")
        self.XACT_WHISPER_API_KEY = settings.get("XACT_WHISPER_API_KEY")
        self.XACT_WHISPER_MODEL = settings.get("XACT_WHISPER_MODEL","distil-medium.en")
        self.XACT_MONGODB_SERVER_URI = settings.get("XACT_MONGODB_SERVER_URI","mongodb://localhost:27017")
        self.XACT_DB_Path = settings.get("XACT_DB_Path",XACT_DB_Path)
        self.XACT_DOC_Path = settings.get("XACT_DOC_Path",XACT_DOC_Path)
        self.XACT_VEC_DB_Path = settings.get("XACT_VEC_DB_Path",XACT_VEC_DB_Path)
        logger.info("xact.settings.Config_Server initialized with API endpoints.")
        self.AUDIO_CHUNK = settings.get("AUDIO_CHUNK", 1024)
        self.AUDIO_FORMAT = settings.get("AUDIO_FORMAT", pyaudio.paInt16)
        self.AUDIO_CHANNELS = settings.get("AUDIO_CHANNELS", 1)
        self.AUDIO_RATE = settings.get("AUDIO_RATE", 24000)
        logger.info("xact.settings.Config_speech_reg audio parameters set.")


    def get_dir(self, doc):
        return self.XACT_DOC_Path /doc
    
    def get_database_name(self):
        return "xactdb"



# Initialize and use settings
settings = Settings()
config = Config(settings)


# Ensure settings are saved when the app closes
import atexit
atexit.register(lambda: settings.save())
