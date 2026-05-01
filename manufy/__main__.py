import argparse
import subprocess

from . import __author__, __version__
from .lib import (
    LEARNING_GOALS,
    STUDY_CHECKLIST,
    course_manual,
    course_overview,
    tutor_instructions,
)
from .settings import Settings

DESC = "Create modified docs files (in mdocs folder) for course manual & tutor instructions"

USAGE = DESC + """

* modified topics qmd file (with/without questions,
    with/without instructions for tutors)
* sym-links of all other files

Definitions for qmd files:

* Topic file are defined by the name: `[two letters]_[topic].qmd`
* Sections marked with (TM) will be presented for the tutorial meeting
    They will be only shown for students, if specified.
* Answers section: `**Answer**` in tutorial meeting sections
    They will be shown to tutors only
* Tag (in brackets) behind 2nd-level headings can be used to exclude parts
    of the text
    - (tm) for tutorial meeting activity.
          presented later or for tutors, if tag 'tutors' is defined (see below)
    - (tutors) shown to tutors only,
            if that tag is missing in the topic file, not tutor instructions
            will be rendered
    - (skip) always hidden
    - (dev) for develop
"""

def render(folder, to_pdf: bool = False):
    cmd = ["quarto", "render", f"{folder}"]
    if to_pdf:
        cmd.extend(["--to", "pdf"])
    print(f"Render with Quarto: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise RuntimeError("Rendering with Quarto failed. Please check the output above for details.")

def cli():
    parser = argparse.ArgumentParser(
        description=f"make_manuals {__version__}: {DESC}",
        epilog=f"(c) {__author__}")

    parser.add_argument("TOML", help="path to the toml file for the manual settings (default: manual.toml)", nargs='?', default="")

    parser.add_argument("TOPICS", nargs='*',
                        help="List of topics that should be visible in the course manual for the students (see also manual.toml). "
                             "If no topics are specified, all topics will be included.")

    parser.add_argument("--course", dest="course_only",
                        action="store_true",
                        help="course_manual only",
                        default=False)

    parser.add_argument("--instructions", dest="instructions_only",
                        action="store_true",
                        help="tutor instructions only",
                        default=False)

    parser.add_argument("--render", dest="render",
                        action="store_true",
                        help="render the generated files with Quarto",
                        default=False)

    parser.add_argument('--develop',  dest="develop",
                        action="store_true",
                        help="development mode for course manual. Extracts everything, also (dev) and (skip). Enforces course manual only.")

    parser.add_argument('--overview',  dest="overview",
                        action="store_true",
                        help=f"make course overview (overview.md). Extracts the subsections '{LEARNING_GOALS}' and '{STUDY_CHECKLIST}' ")

    parser.add_argument("--usage", action="store_true", default=False,
                        help="show usage")

    args = vars(parser.parse_args())

    if args["usage"]:
        parser.print_usage()
        print("\n" + USAGE)
        exit()

    if len(args["TOML"]) < 2:
        print("No TOML file specified.")
        parser.print_help()
        exit()

    settings = Settings(args["TOML"])
    if settings.is_defined():
        print(f"Using settings: {settings.fl_name}")


    if args["overview"]:
        fld = course_overview(settings, "overview.md")
        if args["render"]:
            render(fld, to_pdf=True)
        exit()

    if args["develop"]:
        course_manual(settings, tm_visible=[''], develop_mode=True)
        exit()

    if not args["course_only"]:
        fld = tutor_instructions(settings)
        if args["render"]:
            render(fld, to_pdf=True)

    if not args["instructions_only"]:
        tm_visible = list(settings.get("tm_visible", []))
        fld = course_manual(settings, tm_visible=tm_visible)
        if args["render"]:
            render(fld, to_pdf=False)


if __name__ == "__main__":
    cli()
