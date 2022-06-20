from typing import Any
import logging

from utils.ConfigReader import ConfigClass, ConfigError

class LoggerError(Exception): pass
class UnknownLogLevel(LoggerError, ValueError): pass
class NotSetLogLevel(ConfigError, LoggerError, ValueError): pass

class LoggerClass():
    class _LogColors: #
        Header = '\033[95m'

        OkBlue = '\033[94m'
        OkCyan = '\033[96m'
        OkGreen = '\033[92m'

        Warning = '\033[93m'
        Error = '\033[91m'
        Broke = '\033[91m\033[1m\033[4m'

        End = '\033[0m'

        Bold = '\033[1m'
        Underline = '\033[4m'

    def __init__(self, Config: ConfigClass):
        self.__Config = Config.Config
        #                          1        2        3         4         5
        self.__Levels = ["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        self.__NeedIndent = False
        self.__LoggingConfigured = False

        try: self.__CurrentLevel: str = self.__Config['Log']['Level']
        except Exception: 
            self.Log("Error while loading logging system. Log level not set in config.yaml", "CRITICAL")
            raise NotSetLogLevel()

        if(self.__CurrentLevel not in self.__Levels):
            self.Log("Error while loading logging system. Unknown log level", "CRITICAL")
            raise UnknownLogLevel()


        try: self.__Colorise: bool = self.__Config['Log']['Colorise']
        except Exception: 
            self.Log("Not found color flag in config.yaml. Colorise output disabled", "WARNING")
            self.__Colorise = False

        try: self._LogFileName = self.__Config['Log']['FileName']
        except Exception: 
            self.Log("Log file name not found in config.yaml. Using 'main.log' as default", "WARNING")
            self._LogFileName = "main.log"

        logging.basicConfig(level = self.__LevelForLogging(self.__CurrentLevel), 
                            filename = "./"+self._LogFileName, 
                            filemode = "w", 
                            format = '{App}     [%(asctime)-18s] (%(levelname)-8s): %(message)s', 
                            datefmt = '%d-%b-%y %H:%M:%S')
        self.__LoggingConfigured = True
        
        self.Log("Logger init - OK", 2)

    def __LevelForLogging(self, Level: str) -> str: 
        if(Level == "ALL"): return "NOTSET"
        else: return Level

    def Log(self, Message: str, Level: str | int ="INFO") -> None:
        if(isinstance(Level, str) and (Level not in self.__Levels)): self.Log(Message, Level="INFO")
        if(isinstance(Level, int)):
            if(Level < 0 or Level > len(self.__Levels)): self.Log(Message, Level="INFO")
            else: self.Log(Message, Level=self.__Levels[Level])

        # Level next type only 'str'
        if(isinstance(Level, str)):
            if(self.__Levels.index(Level) < self.__Levels.index(self.__CurrentLevel)): return

            if(self.__Colorise): 
                if(Level == "DEBUG"): print(f"{self._LogColors.OkBlue}", end="")
                if(Level == "INFO"): print(f"{self._LogColors.Bold}", end="")
                if(Level == "WARNING"): print(f"{self._LogColors.Warning}", end="")
                if(Level == "ERROR"): print(f"{self._LogColors.Error}", end="")
                if(Level == "CRITICAL"): print(f"{self._LogColors.Broke}", end="")
            else: print(f"({Level}): ", end="")

            print(f"{Message}", end="")
            if(self.__LoggingConfigured):
                if(Level == "DEBUG"): logging.debug(Message)
                if(Level == "INFO"): logging.info(Message)
                if(Level == "WARNING"): logging.warning(Message)
                if(Level == "ERROR"): logging.error(Message)
                if(Level == "CRITICAL"): logging.critical(Message)

            if(self.__Colorise): print(f"{self._LogColors.End}", )
            else: print()

            if(Level != "DEBUG"): self.__NeedIndent = True

    def DebugPrint(self, *Messages: Any):
        if(self.__Colorise): print(f"{self._LogColors.OkBlue}")
        print(f"{' '.join([str(i) for i in Messages])}")
        if(self.__Colorise): print(f"{self._LogColors.End}")

    def Indent(self): 
        if(self.__NeedIndent): 
            print() 
            self.__NeedIndent = False
    def Detach(self): 
        if(self.__NeedIndent): 
            print(f"\n--- --- --- --- ---\n")
            self.__NeedIndent = False

