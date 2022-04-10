import logging
import logging.handlers

if __name__ == "__main__":
    try:
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)
        fh = logging.handlers.RotatingFileHandler(filename="file.log",
                                                    maxBytes=10485760,
                                                    backupCount=10)
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)f - %(levelname)s - %(message)s")
        logger.addHandler(fh)

        logger.info("Main Started")

    except Exception as e:
        logger.error(f"main_logging:main:{e}")