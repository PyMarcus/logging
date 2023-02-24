import logging
import sys
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from inspect import currentframe, getouterframes
from datetime import datetime
from typing import Any, List
from dataclasses import dataclass, field


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class FormatString:
    """Log format to show
    Time, Level, Message, Separator=','"""
    TIME: str = field(default="%(asctime)s")
    LEVEL: str = field(default="%(levelname)s")
    MESSAGE: str = field(default="%(message)s")
    SEPARATOR: str = field(default="-")


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class Levels:
    """Levels to add into log description
    INFO, DEBUG, ERROR, WARNING, CRITICAL"""
    INFO: str = field(default="INFO")
    DEBUG: str = field(default="DEBUG")
    WARNING: str = field(default="WARNING")
    ERROR: str = field(default="ERROR")
    CRITICAL: str = field(default="CRITICAL")


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class GenericalLogging:
    """
    "Class for to create a log file to systems
    :param path: path to save
    :param name: name of log, by default the name from application
    """
    path: str
    name: str = field(default=sys.argv[0].split('/')[-1].split('.')[0])
    __local_path: str = field(default='.', init=False)
    identifier: bool = field(default=False, init=False)
    _was_called: Any = field(default=None)

    def __build_log_name(self) -> str:
        the_name: str = self.name + '_' + str(datetime.now()).split(' ')[0] + '.log'
        if len(self.path) <= 1:
            return os.path.join(self.__local_path, the_name)
        return os.path.join(self.path, the_name)

    def minimal_log(self, message: str, level: str = "I", format: str =
    "%(asctime)s::%(levelname)s::%(message)s") -> str | None:
        """
        For debug. If no parameter is specified then info will be set
        [IT´s CANNOT BE USED WITH OTHERS METHODS]
        :param message
        :param level: I -> INFO, E -> ERROR, C -> CRITICAL, W -> WARNING, D -> DEBUG
        :param format: Format of messasge, if no specified, then all formats will be used
        :return: None
        """
        try:
            assert level.upper() in ["I", "E", "C", "W", "D"]
            match level:
                case "I":
                    logging.basicConfig(level=Levels.INFO, format=format)
                    logging.info(message)
                case "E":
                    logging.basicConfig(level=Levels.ERROR, format=format)
                    logging.error(message)
                case "C":
                    logging.basicConfig(level=Levels.CRITICAL, format=format)
                    logging.critical(message)
                case "W":
                    logging.basicConfig(level=Levels.WARNING, format=format)
                    logging.warning(message)
                case "D":
                    logging.basicConfig(level=Levels.DEBUG, format=format)
                    logging.debug(message)
            self._was_called = currentframe()
        except AssertionError:
            print("Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for format")
            return "Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG) "

    def minimal_log_file(self, message: str, level: str = "I", format: str =
    "%(asctime)s::%(levelname)s::%(message)s") -> str | None:
        """
        Save log file. If no parameter is specified then info will be set
        :param message
        :param level: I -> INFO, E -> ERROR, C -> CRITICAL, W -> WARNING, D -> DEBUG
        :param format: Format of messasge, if no specified, then all formats will be used
        :return: None
        """
        try:
            calframe = getouterframes(self._was_called, 2)
            if calframe[0].function == "minimal_log":
                raise Exception("Please, remove or comment the minimal_log call!")
        except IndexError:
            ...
        try:
            assert level.upper() in ["I", "E", "C", "W", "D"]
            match level:
                case "I":
                    logging.basicConfig(level=Levels.INFO, format=format, filename=self.__build_log_name())
                    logging.info(message)
                case "E":
                    logging.basicConfig(level=Levels.ERROR, format=format, filename=self.__build_log_name())
                    logging.error(message)
                case "C":
                    logging.basicConfig(level=Levels.CRITICAL, format=format, filename=self.__build_log_name())
                    logging.critical(message)
                case "W":
                    logging.basicConfig(level=Levels.WARNING, format=format, filename=self.__build_log_name())
                    logging.warning(message)
                case "D":
                    logging.basicConfig(level=Levels.DEBUG, format=format, filename=self.__build_log_name())
                    logging.debug(message)
        except AssertionError:
            print("Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for format")
            return "Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG) "

    def logging_this(self, message: str, new_name: None | str = None,
                     level: str = "I", formater: List[str] = None,
                     time_format: str = "%Y-%m-%d %H:%M:%S") -> str | None:
        """
        Most recommended!
        Allows you to configure the log
        :param time_format: default: %Y-%m-%d %H:%M:%S
        :param formater: ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]...
        :param message: text that will be saved
        :param new_name: not obligatory
        :param level: I -> INFO, E -> ERROR, C -> CRITICAL, W -> WARNING, D -> DEBUG
        :return: None
        """
        try:
            calframe = getouterframes(self._was_called, 2)
            if calframe[0].function == "minimal_log":
                raise Exception("Please, remove or comment the minimal_log call!")
        except IndexError:
            ...
        try:
            assert level.upper() in ["I", "E", "C", "W", "D"]
            assert self.__contain(formater, ["A", "M", "T", "L"]) == True

            if new_name is None:
                new_name = self.__build_log_name()

            # settings
            format = FormatString.SEPARATOR.join(self.__converter(formater))
            logger = logging.getLogger(new_name)

            match level:
                case "I":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings(time_format, format, logger)
                    logger.info(message)
                case "E":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings(time_format, format, logger)
                    logger.error(message)
                case "C":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings(time_format, format, logger)
                    logger.critical(message)
                case "W":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings(time_format, format, logger)
                    logger.warning(message)
                case "D":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings(time_format, format, logger)
                    logger.debug(message)
        except AssertionError:
            print("""Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater""")
            return """Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater"""

    def logging_this_with_rotating(self, message: str, new_name: None | str = None,
                                   level: str = "I", formater: List[str] = None,
                                   time_format: str = "%Y-%m-%d %H:%M:%S",
                                   max_bytes: int = None, backup_count: int = None) -> str | None:
        """
        Most recommended!
        Allows you to configure the log with rotation
        :param backup_count: limit of log files
        :param max_bytes: max size for file
        :param time_format: default: %Y-%m-%d %H:%M:%S
        :param formater: ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]...
        :param message: text that will be saved
        :param new_name: not obligatory
        :param level: I -> INFO, E -> ERROR, C -> CRITICAL, W -> WARNING, D -> DEBUG
        :return: None
        """
        try:
            calframe = getouterframes(self._was_called, 2)
            if calframe[0].function == "minimal_log":
                raise Exception("Please, remove or comment the minimal_log call!")
        except IndexError:
            ...
        try:
            assert level.upper() in ["I", "E", "C", "W", "D"]
            assert self.__contain(formater, ["A", "M", "T", "L"]) == True

            if new_name is None:
                new_name = self.__build_log_name()

            # settings
            format = FormatString.SEPARATOR.join(self.__converter(formater))
            logger = logging.getLogger(new_name)

            match level:
                case "I":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_rotating(new_name, time_format, format,
                                                             logger, max_bytes, backup_count)
                    logger.info(message)
                case "E":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_rotating(new_name, time_format, format,
                                                             logger, max_bytes, backup_count)
                    logger.error(message)
                case "C":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_rotating(new_name, time_format, format,
                                                             logger, max_bytes, backup_count)
                    logger.critical(message)
                case "W":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_rotating(new_name, time_format, format,
                                                             logger, max_bytes, backup_count)
                    logger.warning(message)
                case "D":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_rotating(new_name, time_format, format,
                                                             logger, max_bytes, backup_count)
                    logger.debug(message)
        except AssertionError:
            print("""Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater""")
            return """Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater"""

    def __define_settings_rotating(self, name: str, time_format: str, format: str, logger: Any,
                                   max_bytes: int = None, backup: int = None) -> Any:
        if max_bytes and backup:
            file_handler = RotatingFileHandler(name, maxBytes=max_bytes, backupCount=backup)
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
            return logger
        elif max_bytes and not backup:
            file_handler = RotatingFileHandler(name, maxBytes=max_bytes)
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
            return logger
        elif backup and not max_bytes:
            file_handler = RotatingFileHandler(name, backupCount=backup)
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            file_handler.namer = lambda name: name.replace(".log", '') + ".log"
            logger.addHandler(file_handler)
            return logger
        else:
            file_handler = RotatingFileHandler(name)
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            file_handler.namer = lambda name: name.replace(".log", '') + ".log"
            logger.addHandler(file_handler)
            return logger

    def logging_this_with_time_rotating(self, message: str, new_name: None | str = None,
                                        level: str = "I", formater: List[str] = None,
                                        time_format: str = "%Y-%m-%d %H:%M:%S",
                                        interval: int = None, backup_count: int = None,
                                        when: str = 'd') -> str | None:
        """
        Most recommended!
        Allows you to configure the log with time rotation
        :param interval: interval of days
        :param when: frequency to create a file: "d" -> daily, "midnight", "s" -> seconds
        :param backup_count: limit of log files
        :param time_format: default: %Y-%m-%d %H:%M:%S
        :param formater: ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]...
        :param message: text that will be saved
        :param new_name: not obligatory
        :param level: I -> INFO, E -> ERROR, C -> CRITICAL, W -> WARNING, D -> DEBUG
        :return: None
        """
        try:
            calframe = getouterframes(self._was_called, 2)
            if calframe[0].function == "minimal_log":
                raise Exception("Please, remove or comment the minimal_log call!")
        except IndexError:
            ...
        try:
            assert level.upper() in ["I", "E", "C", "W", "D"]
            assert self.__contain(formater, ["A", "M", "T", "L"]) == True

            if new_name is None:
                new_name = self.__build_log_name()

            # settings
            format = FormatString.SEPARATOR.join(self.__converter(formater))
            logger = logging.getLogger(new_name)

            match level:
                case "I":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_time_rotating(new_name, time_format, format,
                                                                  logger, when, backup_count, interval)
                    logger.info(message)
                case "E":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_time_rotating(new_name, time_format, format,
                                                                  logger, when, backup_count, interval)
                    logger.error(message)
                case "C":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_time_rotating(new_name, time_format, format,
                                                                  logger, when, backup_count, interval)
                    logger.critical(message)
                case "W":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_time_rotating(new_name, time_format, format,
                                                                  logger, when, backup_count, interval)
                    logger.warning(message)
                case "D":
                    logger.setLevel(Levels.INFO)
                    logger = self.__define_settings_time_rotating(new_name, time_format, format,
                                                                  logger, when, backup_count, interval)
                    logger.debug(message)
        except AssertionError:
            print("""Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater""")
            return """Invalid option! Try: I (INFO), E (ERROR), C (CRITICAL), W(WARNING), D (DEBUG), for Level or
                  ["A"] -> all (TIME, LEVEL, MESSAGE) -> ["T", "L"], ["T", "M"]... for Formater"""

    def __define_settings_time_rotating(self, name: str, time_format: str, format: str, logger: Any,
                                        when: str = 'd', backup: int = None, interval: int = 1) -> Any:
        if backup:
            file_handler = TimedRotatingFileHandler(name, backupCount=backup, when=when, interval=interval)
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            file_handler.namer = lambda name : name.replace(".log", '') + ".log"
            logger.addHandler(file_handler)
            return logger
        else:
            file_handler = TimedRotatingFileHandler(name, when=when, interval=interval)
            file_handler.namer = lambda name : name.replace(".log", '') + ".log"
            console_formatter = logging.Formatter(format, datefmt=time_format)
            file_handler.setFormatter(console_formatter)
            logger.addHandler(file_handler)
            return logger

    @staticmethod
    def __define_settings(time_format: str, format: str, logger: Any) -> Any:
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(format, datefmt=time_format)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        return logger

    @staticmethod
    def __contain(item: Any, compare: Any) -> bool:
        count: int = 0
        for i in item:
            if i in compare:
                count += 1
        if count == len(item):
            return True
        return False

    @staticmethod
    def __converter(formater: List[str]) -> List[str]:
        content: List[str] = []
        for letter in formater:
            match letter:
                case 'T':
                    content.append(FormatString.TIME)
                case 'M':
                    content.append(FormatString.MESSAGE)
                case 'L':
                    content.append(FormatString.LEVEL)
                case 'A':
                    content.append(FormatString.TIME)
                    content.append(FormatString.LEVEL)
                    content.append(FormatString.MESSAGE)
        return content


if __name__ == '__main__':
    g = GenericalLogging('.')
    # g.minimal_log("hello, world!", level="E")
    # g.minimal_log_file("hello, world!", level="D")
    # g.logging_this("hello, world!", level="I", formater=["A"])
    # g.logging_this_with_rotating("ok", level="I", formater=["A"])
    g.logging_this_with_time_rotating("ok", level="I", formater=["A"], when="s", interval=1)
