"""Creating course manuals and tutor instruction with Quarto

Oliver Lindemann
"""

__version__ = "0.9.2"
__author__ = "Oliver Lindemann"

import sys as _sys

from .lib import course_manual, course_overview, tutor_instructions

if _sys.version_info[0] != 3 or _sys.version_info[1] < 11:

    raise RuntimeError("make manual {0} ".format(__version__) +
                      "is not compatible with Python {0}.{1}.".format(
                                                    _sys.version_info[0],
                                                    _sys.version_info[1]) +
                      "\n\n  Please use Python 3.11 or later.")

