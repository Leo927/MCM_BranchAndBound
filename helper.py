import logging
def get_logger():
    logger = logging.getLogger('MCM')
    if logger.hasHandlers():
        return logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('log.txt', mode='w')
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger
