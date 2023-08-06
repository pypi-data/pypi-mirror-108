
from __future__ import annotations

import typing as _T

from rlogging import formaters, handlers, loggers, printers

LOGGING_LEVELS = {
    0: 'RUBBISH',
    20: 'DEBUG',
    40: 'INFO',
    60: 'WARNING',
    80: 'ERROR',
    100: 'CRITICAL',
}


loggersDict: dict[str, loggers.BaseLogger] = {}


def registration_logger(loggerName: str, loggerType: _T.Type[loggers.BaseLogger]):
    """ Регистрация нового логера с неким типом

    Args:
        loggerName (str): Имя логера
        loggerType (_T.Type[loggers.BaseLogger]): Тип логера

    """

    loggersDict[loggerName] = loggerType(loggerName)


def get_logger(loggerName: str) -> _T.Union[loggers.BaseLogger, loggers.Logger]:
    """ Получение логера.

    Если логер не создан - создание.

    Args:
        loggerName (str): Имя логера

    """

    if loggerName not in loggersDict:
        raise KeyError('Логгер {0} не зарегистрирован'.format(
            loggerName
        ))

    return loggersDict[loggerName]


def construct_logger(loggerName: str, ):
    """ Создание логера

    До создания, все логи хранятся в памяти основного потока.

    После создания логера, очередь передастся в Хендлеры.

    """


def __start_printers(printersPool: printers.PrintersPool):
    for printer in printersPool.printers:
        printer.start()


def __start_handlers(handlersPool: handlers.HandlersPool):
    for handler in handlersPool.handlers:
        if handler.printersPool is None:
            raise AttributeError('Попытка запустить хендлер ({0}), у которого не установлен пул принтеров'.format(
                handler.__class__.__name__
            ))

        __start_printers(handler.printersPool)

        handler.start()


def start_loggers():
    """ Остановка всех логеров и их хендлеров

    Raises:
        AttributeError: Попытка запустить логер или хендлер, которые будет бесполезны

    """

    for _, logger in loggersDict.items():
        if logger.handlersPool is None:
            raise AttributeError('Попытка запустить логер ({0}), у которого не установлен пул хендлеров'.format(
                logger.name
            ))

        __start_handlers(logger.handlersPool)
        logger.start()


def stop_loggers():
    """ Остановка всех логеров и их хендлеров """

    for _, logger in loggersDict.items():

        __stop_handlers(logger.handlersPool)

        if logger._started:
            logger.stop()


def __stop_handlers(handlersPool: handlers.HandlersPool):
    """ Остановка хендлеров

    Args:
        handlersPool (handlers.HandlersPool): Пул хендлеров, которые нужно остановить

    """

    if handlersPool is None:
        return

    for handler in handlersPool.handlers:
        __stop_printers(handler.printersPool)
        if handler._started:
            handler.stop()


def __stop_printers(printersPool: printers.PrintersPool):
    """ Остановка принтеров

    Args:
        printersPool (printers.PrintersPool): Пул принтеров, которые нужно остановить

    """

    if printersPool is None:
        return

    for printer in printersPool.printers:
        if printer._started:
            printer.stop()


registration_logger('mainLogger', loggers.Logger)
