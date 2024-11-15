import json
import logging.config
import pathlib

def setup_logging():
    # Get the directory of the current file
    current_dir = pathlib.Path(__file__).parent
    # Construct the path to config.json
    config_file = current_dir / "config.json"
    
    # Ensure the config file exists
    if not config_file.is_file():
        raise FileNotFoundError(f"Logging configuration file not found: {config_file}")
    
    # Load the configuration
    with open(config_file, 'r') as f_in:
        config = json.load(f_in)
    
    # Apply the logging configuration
    logging.config.dictConfig(config)
