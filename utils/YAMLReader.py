from typing import Any
import yaml
import codecs
from pathlib import Path

class YAMLReaderClass:
    class YamlIncorrectSyntax(Exception): pass 
    
    def ReadYamlFile(self, PathToFile: str) -> dict[str, Any]:
        try:
            with codecs.open(str(Path(__file__).parents[0] / Path(PathToFile)), encoding='utf-8') as YAMLFile:
                return yaml.safe_load(YAMLFile)
        except Exception:
            raise YAMLReaderClass.YamlIncorrectSyntax()

    def TryGetNesting(self, Object: dict[str, Any], key: str) -> Any:
        try: return Object[key]
        except Exception: pass