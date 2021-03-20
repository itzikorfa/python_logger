import logging
import advance_logger


def foo(x):
    x = x**4
    logger.dblog(x)
    return x


if __name__ == '__main__':
    logger = advance_logger.init_logger()
    logger.proxylog("testing")
    foo(3)
