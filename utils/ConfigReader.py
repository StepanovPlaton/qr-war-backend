from pathlib import Path

from utils.YAMLReader import *

class ConfigError(Exception): pass
class ConfigNotFound(ConfigError, FileNotFoundError): pass

class ConfigClass():
    def __init__(self, YAMLReader: YAMLReaderClass, PathToConfig: str ="..\\config.yaml", quiet: bool =False) -> None: 
        try:
            self.Config = YAMLReader.ReadYamlFile(PathToConfig)
        except Exception:
            if(not quiet): print("Error while reading config.yaml")
            raise ConfigNotFound()

        self.Config["ParserRootPath"] = Path(__file__).parents[1]

        if(not quiet): print("Config attach")