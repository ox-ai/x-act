import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pydantic import BaseModel


class Config:
    def __init__(self, default_config: Dict[str, Optional[Any]]):
        """
        Initializes the Config class with a default dictionary.

        Args:
            default_config (Dict[str, Optional[Any]]): Default key-value pairs for configuration.
        """
        self.default_config = default_config
        self.config = default_config.copy()

    @staticmethod
    def _serialize_value(value: Any) -> str:
        """Serialize a value to a string for storing in .env files."""
        if isinstance(value, (list, dict)):
            return json.dumps(value)  # Serialize lists and dicts as JSON strings
        return str(value) if value is not None else ""
    @staticmethod
    def _deserialize_value(value: str) -> Any:
        """Deserialize a string from .env into its original type."""
        try:
            # Attempt to parse JSON strings back into Python objects
            return json.loads(value)
        except json.JSONDecodeError:
            # If not JSON, return the raw string
            return value
        
    @staticmethod
    def load_env(dotenv_path: Optional[str] = ".env",var_list: Optional[list[str]]=None):
        """Load environment variables from a .env file."""
        if dotenv_path and os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)

            existing_env = {}
            with open(dotenv_path, "r") as file:
                for line in file:
                    line = line.strip()
                    if line and "=" in line:
                        key, value = line.split("=", 1)
                        existing_env[key.strip()] = Config._deserialize_value(value.strip())

            # Update with environment variables
            if var_list:
                for key in var_list:
                    env_value = os.getenv(key)
                    if env_value is not None:
                        existing_env[key] = Config._deserialize_value(env_value)

        else: 
            existing_env ={}

        return existing_env
    
    def update(self,default_config: Dict[str, Optional[Any]]):
        self.config.update(default_config)

    def load(self, dotenv_path: Optional[str] = ".env", json_path: Optional[str] = None):
        """
        Load configuration from a .env file or a JSON file and update the config dictionary.

        Args:
            dotenv_path (Optional[str]): Path to the .env file (default is ".env").
            json_path (Optional[str]): Path to a JSON configuration file.
        """
        # Load .env file if it exists
        if dotenv_path and os.path.exists(dotenv_path):

            existing_env = Config.load_env(dotenv_path=dotenv_path,var_list=list(self.default_config.keys()))
            for key,value in existing_env.items():
                self.config[key]=value

        # Load JSON file if specified and exists
        if json_path and os.path.exists(json_path):
            with open(json_path, "r") as json_file:
                json_data = json.load(json_file)
                for key, value in json_data.items():
                    if key in self.config:
                        # Prioritize env variables, fall back to JSON
                        if self.config[key] is None:
                            self.config[key] = value


    def generate(self, dotenv_path: Optional[str] = ".env", json_path: Optional[str] = None):
        """
        Generate or update .env or JSON files with default configuration values.

        Args:
            dotenv_path (Optional[str]): Path to the .env file (default is ".env").
            json_path (Optional[str]): Path to a JSON configuration file.
        """
        if os.path.exists(dotenv_path):
            existing_env = Config.load_env(dotenv_path)
            # Add missing keys
            with open(dotenv_path, "w") as file:
                for key, value in self.default_config.items():
                    default_serialized_value = Config._serialize_value(value)
                    if key not in existing_env:
                        serialized_value = default_serialized_value
                        file.write(f"{key}={serialized_value}\n")
                    else:
                        upenv_value = existing_env[key] if existing_env[key] else default_serialized_value
                        file.write(f"{key}={upenv_value}\n")

        # Handle JSON file
        if json_path:
            json_path = Path(json_path)  # Ensure it's a Path object

            # If the path is a directory, append "config.json"
            if json_path.is_dir():
                json_path = json_path / "config.json"

            # Ensure parent directories exist
            json_path.parent.mkdir(parents=True, exist_ok=True)

            # Load existing config if the file exists
            existing_json = {}
            if json_path.exists():
                with open(json_path, "r") as file:
                    existing_json = json.load(file)
            # Add missing keys
            for key, value in self.default_config.items():
                if key not in existing_json:
                    existing_json[key] = value
                else:
                    if not existing_json[key]:
                        existing_json[key]= value
            # Save updated JSON
            with open(json_path, "w") as file:
                json.dump(existing_json, file, indent=4)

    def get_class(self):
        """
        Returns a dynamically created class where attributes are derived from the config dictionary.

        Returns:
            type: A dynamically created class with attributes from the config dictionary.
        """
        config_dict = self.config

        class ConfigClass():
            def __init__(self):
                for key, value in config_dict.items():
                    setattr(self, key, value)

            def __repr__(self):
                class_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
                return f"<{class_name} {self.__dict__}>"
            
            def add_method(self, method):
                """
                Dynamically add a method to this instance.

                Args:
                    method (function): A function to be added as a method.
                """
                import types
                setattr(self, method.__name__, types.MethodType(method, self))

        return ConfigClass
    
    def get(self):
        return self.get_class()()
    
    def __repr__(self):
        class_name =f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        return f"<{class_name} {self.config}>"


class ConfigVar:
    def __init__(self,var:Any=None,config_var:Any=None):
        self.var = var 
        self.config_var= config_var
        self.is_config_var = False
        if not var:
            self.is_config_var = True

    def get(self,var:Any=None,config_var:Any=None):
        if self.is_config_var:
            return config_var or self.config_var
        else:
            return var or self.var
        
    def __call__(self,var:Any=None,config_var:Any=None, *args, **kwds):
        # Call get method with args and kwargs
        return self.get(var=var,config_var=config_var,*args, **kwds)
    

    def __repr__(self):
        return self.get()


