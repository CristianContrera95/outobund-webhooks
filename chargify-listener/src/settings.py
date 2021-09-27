from dotenv import load_dotenv
import logging

load_dotenv()

LOGGER_NAME = 'outbound_chargify_listener'
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)
