import re

TM_ALT_TEXT = """#### Tutorial meeting

Information about the activities during the tutorial group
meeting will appear here briefly before the meeting.\n"""

#tags
TAG_TUTORS = "tutors"
TAG_SKIP = "skip" # never included also not in tutor instructions
TAG_DEV = "dev" # currently dev and skip are treated the same
TAG_TM = "tm" # tutor meeting

# folder
BUILD = "_build"

# regular expressions
class RE():
    """Regular expressions"""
    # TAGS
    tutors = re.compile(r"\(" + TAG_TUTORS + r"\)", re.IGNORECASE & re.MULTILINE) # [text] (TAG)..$
    tags = re.compile(r"^(.+) \((.+)\)\s*$", re.IGNORECASE) # (text) (TAG)..$
    topic_filename = re.compile(r"^\w\w_(\w+)\.qmd$") # [digit][letters]_[topic].qmd
    #parser
    first_level_heading = re.compile(r"^\s*#\s+(.+)")
    second_level_heading = re.compile(r"^\s*##\s+(.+)")
    new_task = re.compile(r"^\s*###\s+(Question|Discussion|Station|Activity)") # "### Question/Discussion/Activity ..."
    answer = re.compile(r"^\s*\*\*Answer\*\*") # "**Answer**"
