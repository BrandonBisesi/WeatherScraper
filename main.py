"""Module containing logger for application."""
import logging
import logging.handlers
from weather_processor import WeatherProcessor

def main_log():
    """Creates the logger."""
    try:
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename='file.log')
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)

        logger.info("Main Started")

        proc = WeatherProcessor()
        proc.prompt_user()

    except Exception as error:
        logger.error("main_log:%s",error)

if __name__ == "__main__":
    main_log()
