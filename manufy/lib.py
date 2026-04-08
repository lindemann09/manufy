from pathlib import Path
from typing import List, Optional, Union

from .files import Files
from .settings import Settings

LEARNING_GOALS = "Learning Objectives"
STUDY_CHECKLIST = "Study Checklist"

def tutor_instructions(settings: Settings) -> Path:
    """processes the qmd files in the docs folder"""

    return course_manual(settings,tutor_instr=True, develop_mode=False)


def course_manual(settings: Settings,
                  tm_visible: Optional[List[str]] = None,
                  tutor_instr=False,
                  develop_mode=False) -> Path:
    """processes the qmd files in the docs folder

        tm_info: list of ids of tutorial meeting sections that should be
                visible
        develop_mode: builds everything and ignores tags to omit section

    returns the build folder as Path object
    """
    files = Files(settings)
    files.prepare_build_folder()
    if tm_visible is None:
        tm_visible = []
    if settings.is_defined():
        tm_visible.extend(settings.get_due_topics())

    if tutor_instr:
        instr_folder = files.tutor_instr
    else:
        instr_folder = files.course_man
    target_folder = files.BUILD.joinpath(instr_folder)
    print(f"create {target_folder}")

    fdb_topic = ""
    for man_doc in files.docs_files(sort_topics_by_date=True):
        # destination file
        dest = files.build_docs_mod_path(man_doc, subfolder=instr_folder)

        if len(man_doc.topic_id) > 0:
            # topic file
            show_tm_info = man_doc.topic_id in tm_visible
            fb = f"- {man_doc.topic_id} "
            if tutor_instr and man_doc.has_tutor_instr():
                fb += "TUTOR INSTR"
            elif show_tm_info:
                fb += "--MEETING--"
            elif develop_mode:
                fb += "   dev     "
            else:
                fb += "  hidden   "
            # extract text
            txt = man_doc.extract_text(tutor_instr=tutor_instr,
                                       develop_mode=develop_mode,
                                       show_tm_infos=show_tm_info)
            txt = "".join(txt)
            if Files.different_content(dest, txt):
                fb += f" changed: {dest}"
                with open(dest, "w", encoding="utf-8") as fl:
                    fl.write(txt)
            fdb_topic += f"{fb}\n"
        else:
            # no a topic file -> make link
            try:
                dest.symlink_to(man_doc.filename.absolute())
            except FileExistsError:
                pass

    if len(fdb_topic) > 0:
        print(fdb_topic)

    return target_folder

def course_overview(settings: Settings, dest_file:Union[str, Path]) -> Path:
    """creates overview MD file

    returns the path to the created file
    """
    files = Files(settings)
    # sort docs_list, take first topic from get_topic_dates then the rest
    doc_list = files.docs_files(sort_topics_by_date=True)
    content = []
    for man_doc in doc_list:
        if len(man_doc.topic_id):
            lg = man_doc.extract_2nd_level_section(LEARNING_GOALS)
            sc = man_doc.extract_2nd_level_section(STUDY_CHECKLIST)
            if len(sc)>0 or len(lg)>0:
                content.extend(man_doc.first_level_headings())
                content.append("\n\n")
                content.extend(lg)
                content.append("\n")
                content.extend(sc)
                content.append("\n\n")

    files.prepare_build_folder()
    dest_file = files.BUILD.joinpath(dest_file)
    with open(dest_file, "w", encoding="utf-8") as fl:
        fl.writelines(content)

    print(f"created {dest_file}")
    return dest_file