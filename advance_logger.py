import logging, os
from logging import handlers
files_and_levels = {
    "info": "info.elg",
    "error" : "error.elg",
    "db" : "db.elg",
    "proxy" : "proxy.elg"
}
LOG_DIR = os.path.join(os.path.dirname(__file__),"logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
DBLOG_LEVELV_NUM = 60
PROXYLOG_LEVELV_NUM = 70

def get_file_name (file_name):
    return os.path.join(LOG_DIR, file_name)


class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level

def dblog(self, message, *args, **kws):
    if self.isEnabledFor(DBLOG_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(DBLOG_LEVELV_NUM, message, args, **kws)


def proxylog(self, message, *args, **kws):
    if self.isEnabledFor(PROXYLOG_LEVELV_NUM):
        # Yes, logger takes its '*args' as 'args'.
        self._log(PROXYLOG_LEVELV_NUM, message, args, **kws)


def init_logger():
    logging.addLevelName(DBLOG_LEVELV_NUM, "dblog")
    logging.Logger.dblog = dblog
    logging.addLevelName(PROXYLOG_LEVELV_NUM, "proxylog")
    logging.Logger.proxylog = proxylog

    logger = logging.getLogger("mylog")

    formatter = logging.Formatter(
        '%(asctime)s | %(name)s |  %(levelname)s: %(message)s')

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)


    info_handler = handlers.TimedRotatingFileHandler(
        filename=get_file_name(files_and_levels["info"]), when='midnight', backupCount=30)
    info_handler.setFormatter(formatter)
    info_handler.setLevel(logging.INFO)
    # info_handler.addFilter(MyFilter(logging.INFO))
    logger.addHandler(info_handler)

    error_handler = handlers.TimedRotatingFileHandler(
        filename=get_file_name(files_and_levels["error"]), when='midnight', backupCount=30)
    error_handler.setFormatter(formatter)
    error_handler.setLevel(logging.ERROR)
    error_handler.addFilter(MyFilter(logging.ERROR))
    logger.addHandler(error_handler)

    db_handler = handlers.TimedRotatingFileHandler(
        filename=get_file_name(files_and_levels["db"]), when='midnight', backupCount=30)
    db_handler.setFormatter(formatter)
    db_handler.setLevel(DBLOG_LEVELV_NUM)
    db_handler.addFilter(MyFilter(DBLOG_LEVELV_NUM))
    logger.addHandler(db_handler)

    proxy_handler = handlers.TimedRotatingFileHandler(
        filename=get_file_name(files_and_levels["proxy"]), when='midnight', backupCount=30)
    proxy_handler.setFormatter(formatter)
    proxy_handler.setLevel(PROXYLOG_LEVELV_NUM)
    proxy_handler.addFilter(MyFilter(PROXYLOG_LEVELV_NUM))
    logger.addHandler(proxy_handler)

    return logger



if __name__ == '__main__':
    log = init_logger()
    import random

    for j in range(40):
        i = random.randint(1,100)
        log.info(f"hi from info {i}")
        log.error(f"hi from error {i}")
        log.dblog(f"hi from db {i}")
        log.proxylog(f"hi from proxy {i}")

