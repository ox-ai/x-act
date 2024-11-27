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
CONFIG_FILE = "settings.json"
XACT_BASE_Path = Path.home() / MASTER_BASE / XACT_BASE 
XACT_DB_Path = XACT_BASE_Path / XACT_DB
XACT_DOC_Path = XACT_BASE_Path / XACT_DOC
XACT_VEC_DB_Path = XACT_BASE_Path / XACT_VEC_DB


XACT_CONFIG_PATH = XACT_BASE_Path / CONFIG_FILE


class Config:
    _instance = None  # Holds the single instance of the class

    # Default values for configuration variables
    XACT_LLM_BASE_URL = "http://localhost:11434/v1/"
    XACT_LLM_API_KEY = "ollama"
    XACT_LLM_MODEL = "qwen2.5-coder:1.5b"
    XACT_LLM_EMBEDDING_MODEL = "nomic-embed-text"
    XACT_WHISPER_BASE_URL = None
    XACT_WHISPER_API_KEY = None
    XACT_WHISPER_MODEL = "distil-medium.en"
    XACT_MONGODB_SERVER_URI = "mongodb://localhost:27017"
    XACT_DB_Path = str(XACT_DB_Path)
    XACT_DOC_Path = str(XACT_DOC_Path)
    XACT_VEC_DB_Path = str(XACT_VEC_DB_Path)
    logger.info("xact.settings.congig initialized with API endpoints.")
    AUDIO_CHUNK =  1024
    AUDIO_FORMAT = pyaudio.paInt16
    AUDIO_CHANNELS =  1
    AUDIO_RATE =  24000
    logger.info("xact.settings.congig audio parameters set.")
    SIM_FORMAT = "dp"
    SIM_FORMATS = ["dp", "ed", "cs"]
    initialized = True  # Mark as initialized

    def __new__(cls):
        # Ensure only one instance of Config exists
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._initialize_defaults(cls._instance)
        return cls._instance

    @classmethod
    def _initialize_defaults(cls, instance):
        # Initialize instance variables with default values
        for attr, value in cls.__dict__.items():
            if not attr.startswith('_') and not callable(value):
                setattr(instance, attr, value)

    def save(self, path):
        """Save the current configuration to a JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        config_data = {k: getattr(self, k) for k in self.__class__.__dict__ if not k.startswith('_') and not callable(getattr(self, k))}
        with open(path, 'w') as f:
            json.dump(config_data, f, indent=4)
        logger.info("Settings saved to JSON.")

    def load(self, path=None):
        """Load configuration from a JSON file and update the instance variables."""
        path = path or XACT_CONFIG_PATH
        if os.path.exists(path):
            with open(path, 'r') as f:
                config_data = json.load(f)
                for k, v in config_data.items():
                    setattr(self, k, v)
            logger.info("Settings loaded from JSON.")
        else:
            logger.info("Settings not loaded from JSON.")
            # raise FileNotFoundError(f"No such configuration file: {path}")
        


    def get_dir(self, doc):
        return self.XACT_DOC_Path /doc
    
    def get_database_name(self):
        return "xactdb"

config = Config()
config.load()

# Ensure settings are saved when the app closes
import atexit
atexit.register(lambda: config.save(XACT_BASE_Path / "settings-updated.json"))
