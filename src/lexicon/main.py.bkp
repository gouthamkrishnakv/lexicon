import os

from lexicon.project import Project
from lexicon.subproject import Subproject

PROJECT_PATH = os.path.join(os.getcwd(), Project.PROJECT_FILE)
SUBPROJECT_PATH = os.path.join(os.getcwd(), Subproject.SUBPROJECT_FILE)


def main():
    if os.path.exists(SUBPROJECT_PATH):
        Subproject.cli_manage()
    elif os.path.exists(PROJECT_PATH):
        Project.cli_manage()
    else:
        Project.cli_generate()
