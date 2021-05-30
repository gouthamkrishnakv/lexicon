import os
import sys

from lexicon.project import Project
from lexicon.subproject import Subproject

PROJECT_PATH = os.path.join(os.getcwd(), Project.PROJECT_FILE)
SUBPROJECT_PATH = os.path.join(os.getcwd(), Subproject.SUBPROJECT_FILE)


def main():
    args = sys.argv
    if os.path.exists(SUBPROJECT_PATH):
        Subproject.cli_manage()
    elif os.path.exists(PROJECT_PATH):
        if len(args) == 1:
            Project.cli_manage()
        else:
            raise NotImplementedError
    else:
        Project.cli_generate()
