import logging
import sys

def setup_logger(name="hive_agent"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Stream to console
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        # Save to file
        fh = logging.FileHandler("agent_activity.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

agent_logger = setup_logger()