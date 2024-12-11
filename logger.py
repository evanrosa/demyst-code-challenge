import logging

# Configure logging to log to both a file and the console
logging.basicConfig(
    level=logging.DEBUG,  # Set the default logging level
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file named 'app.log'
        logging.StreamHandler()          # Logs to the console
    ]
)

# Create a logger object for use in other modules
logger = logging.getLogger(__name__)
