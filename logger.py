import logging

logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)  # ou DEBUG pour plus de détails

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
