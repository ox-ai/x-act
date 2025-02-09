from pathlib import Path
import pyaudio
from xact.config.config import Config
from xact.log.config import log_manager

log_manager.setup_custom_level(level="config",level_num=2)
log = log_manager.init(__name__)

__all__ = ["config"]

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


"""Application-specific configuration class."""

# Default values for configuration variables

default_config = {
    "XACT_LLM_BASE_URL": "http://localhost:11434/v1/",
    "XACT_LLM_API_KEY": "ollama",
    "XACT_LLM_MODEL": "qwen2.5:1.5b ",
    "XACT_LLM_EMBEDDING_MODEL": "nomic-embed-text",
    "XACT_WHISPER_BASE_URL": None,
    "XACT_WHISPER_API_KEY": None,
    "XACT_WHISPER_MODEL": "small",
    "XACT_MONGODB_SERVER_URI": "mongodb://localhost:27017",
    "XACT_DB_Path": str(XACT_DB_Path),
    "XACT_DOC_Path": str(XACT_DOC_Path),
    "XACT_VEC_DB_Path": str(XACT_VEC_DB_Path),
    "AUDIO_CHUNK": 1024,
    "AUDIO_FORMAT": 8,
    "AUDIO_CHANNELS": 1,
    "AUDIO_RATE": 24000,
    "SIM_FORMAT": "dp",
    "SIM_FORMATS": ["dp", "ed", "cs"],
    "TIME_UTF_LOCAL": True,
}

# Create Config instance
gen_config = Config(default_config)

dotenv_path=".env"
json_path="config.json"
# Load configuration from .env or JSON file
gen_config.load(dotenv_path,json_path)

log.info(f"Config loaded from .env:{dotenv_path} json_path : {json_path}" )

# Get dynamically created class and create an object
ConfigClass = gen_config.get_class()
config = ConfigClass()


def get_dir(self, doc):
    """Get the directory path for a specific document."""
    return Path(self.XACT_DOC_Path) / doc


def get_database_name(self):
    """Return the name of the database."""
    return "xactdb"


config.add_method(get_dir)
config.add_method(get_database_name)

log.config(f"Config initilized : {config} \n\n")

UPDATED_CONFIG_Path = XACT_BASE_Path / "updated_config"


# Ensure settings are saved when the app closes
import atexit

# Generate .env or JSON files with default values
atexit.register(
    lambda: gen_config.generate(
        dotenv_path=UPDATED_CONFIG_Path / ".env",
        json_path=UPDATED_CONFIG_Path / "config.json",
    )
)
