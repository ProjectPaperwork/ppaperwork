import logging
from gherkin_paperwork.paperworker import Paperworker

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    """Starting Point
    """ 
    Paperworker = Paperworker()
    Paperworker.work()
