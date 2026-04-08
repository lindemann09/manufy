
from os import listdir
from pathlib import Path
from typing import List

from . import constants as c
from .manual_document import ManualDocument
from .settings import Settings


class Files():
    BUILD = Path(c.BUILD)

    def __init__(self, settings: Settings):
        self.settings = settings
        self.docs_source = Path(settings.get("fld_docs_source")) # type: ignore
        self.course_man = Path(settings.get("fld_course_man"))  # type: ignore
        self.tutor_instr = Path(settings.get("fld_tutor_inst"))  # type: ignore
        self.docs_mod = Path(settings.get("fld_docs_modified")) # type: ignore

    def prepare_build_folder(self):
        # make folders and links to files and subfolder
        for manual in (self.course_man, self.tutor_instr):
            self.BUILD.joinpath(manual.name, self.docs_mod).mkdir(
                parents=True, exist_ok=True)
            for source in manual.iterdir():
                relpath = Path(source.parent.name, source.name)
                try:
                    self.BUILD.joinpath(relpath).symlink_to(source.absolute())
                except FileExistsError:
                    pass

    def docs_files(self, sort_topics_by_date=False) -> List[ManualDocument]:
        """ returns list of all files (ManualDocuments) in source docs folder
            if X.topic id = "" -> no topic file
        """
        rtn: List[ManualDocument] = []
        for d in listdir(self.docs_source):
            if c.RE.topic_filename.match(d):
                topic_id = d.split("_", maxsplit=1)[0]
            else:
                topic_id = ""
            man_doc = ManualDocument(filename=self.docs_source.joinpath(d),
                                     topic_id=topic_id)
            rtn.append(man_doc)

        # sort all by topic id
        rtn = sorted(rtn, key=lambda x: x.topic_id)

        if sort_topics_by_date:
            for topic_id in reversed(self.settings.get_topic_dates().keys()):
                new = []
                while len(rtn) > 0:
                    fl = rtn.pop(0)
                    if fl.topic_id == topic_id:
                        new.insert(0, fl)
                    else:
                        new.append(fl)
                rtn = new
        return rtn

    def build_docs_mod_path(self, man_doc: ManualDocument, subfolder: Path) -> Path:
        return self.BUILD.joinpath(subfolder.name, self.docs_mod, man_doc.filename.name)

    @staticmethod
    def different_content(file_path: Path, content: str):
        """true if text content is different"""
        if file_path.is_file():
            with open(file_path, "r", encoding="utf-8") as fl:
                fl_content = fl.read()
            return hash(fl_content) != hash(content)
        return True
