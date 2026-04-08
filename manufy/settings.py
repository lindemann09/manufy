import tomllib
from collections import OrderedDict
from datetime import date
from pathlib import Path
from typing import Any, Dict


class Settings():

    FILE_ENCODING = "utf-8"
    TM_DATES = "topic-dates"

    def __init__(self, filename:Path|str) -> None:

        self._dict = {}
        self.fl_name = None
        self._read(Path(filename))

    def _read(self, filename:Path):
        """read settings from file"""
        self.fl_name = filename

        if self.fl_name.is_file():
            with open(self.fl_name, "rb") as f:
                try:
                    self._dict = tomllib.load(f)
                except Exception:
                    raise RuntimeError(f"Can't read settings file  {filename}")
        else:
            print(f"WARNING: Settings file {filename} not found.")

    def is_defined(self):
        return len(self._dict) > 0

    def get(self, key:str, default:Any=""):
        try:
            return self._dict[key]
        except KeyError:
            return default

    def get_topic_dates(self) -> OrderedDict[str, date]:
        """returns a dict with tm dates, key is the topic id"""
        d:Dict = self.get(self.TM_DATES, {}) # type: ignore
        return OrderedDict(sorted(d.items(), key=lambda item: item[1]))

    def get_due_topics(self) -> list[str]:
        today = date.today()
        return [k for k,v in self.get_topic_dates().items() \
                if isinstance(v, date) and v<=today]

