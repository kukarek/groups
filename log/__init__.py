from .loggHandler import *

def init(level):

    logging.basicConfig(level=level, filename="log.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
