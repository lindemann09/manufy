from pathlib import Path
from typing import List

from .constants import RE, TAG_DEV, TAG_SKIP, TAG_TM, TAG_TUTORS, TM_ALT_TEXT


class ManualDocument(object):

    def __init__(self, filename:Path, topic_id:str="") -> None:
        self.topic_id = topic_id
        self.filename = filename
        self.__content:List[str] = []  # content of parsed file

    @property
    def content(self) -> List[str]:
        if len(self.__content) == 0:
            # read file
            with open(self.filename, "r", encoding="utf-8") as fl:
                self.__content = fl.readlines()
        return self.__content

    def has_tutor_instr(self):
        """search if any tutor instructions (tutors) are defined in document
        """
        return RE.tutors.search("".join(self.content)) is not None

    def extract_text(self,
                     tutor_instr: bool,
                     show_tm_infos: bool = False,
                     develop_mode: bool = False) -> List[str]:
        rtn = []
        answer_block = False
        skip_part = False
        tag = ""
        show_alt_text = False

        add_tutor_info = tutor_instr and self.has_tutor_instr()

        for l in self.content:
            if RE.second_level_heading.match(l):
                answer_block = False
                # extract tags
                x = RE.tags.match(l)
                if x is None:
                    tag = ""
                else:
                    l, tag = x.groups()  # type: ignore

                if develop_mode:
                    skip_part = tag == TAG_SKIP  # only omit skip-section
                    add_tutor_info = True
                else:
                    skip_part = (tag == TAG_TUTORS and not add_tutor_info) or \
                        tag == TAG_SKIP or \
                        tag == TAG_DEV

                    # skip tutorial meeting info, if not specified to show or no tutor info
                    if (tag == TAG_TM and not show_tm_infos and not add_tutor_info):
                        show_alt_text = True
                        skip_part = True

            if not skip_part:
                if tag == TAG_TM:  # tutorial block
                    # show answers only for tutors
                    if RE.answer.match(l):
                        answer_block = True
                    elif RE.new_task.match(l):
                        answer_block = False
                    if (add_tutor_info or not answer_block):
                        rtn.append(l)
                else:
                    rtn.append(l)

        if show_alt_text and not tutor_instr:
            rtn.append("\n\n" + TM_ALT_TEXT)

        return rtn

    def extract_2nd_level_section(self, heading) -> List[str]:
        rtn = []
        is_section = False
        for l in self.content:
            m = RE.second_level_heading.match(l)
            if m is not None:
                is_section = m.groups()[0].startswith(heading)
            if is_section:
                rtn.append(l)

        return rtn

    def first_level_headings(self):
        """returns all first level headings"""

        rtn = []
        for l in self.content:
            m = RE.first_level_heading.match(l)
            if m is not None:
                rtn.append(m.group())
        return rtn
