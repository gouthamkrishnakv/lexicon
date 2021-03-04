# This holds the information regarding the students for the project needed.

from enum import Enum
import inquirer
import os
from typing import Dict, List, Optional
import yaml


from author import Author
from subproject import Subproject

class ProjectType(Enum):
    ASSIGNMENT = "assignment"
    EXAMINATION = "examination"
    PROJECT = "project"
    PERSONAL = "personal"
    FACULTY_COPY = "faculty copy"
    ANSWER_KEY = "answer key"
    OTHER = "other"

class Project:
    # -- CLASS MEMBERS (INSTANCE VARIABLES) ---
    # project name
    name: str
    # type of project
    type: ProjectType
    # author of the project
    author: Author
    # subprojects
    subprojects: List[Subproject]

    # PROJECT FILE
    PROJECT_FILE = "lexicon.yaml"
    # --- CLASS CONSTANTS ---
    # name of the project
    NAME = "Name"
    # this holds the type of project, check ProjectType class
    TYPE_OF_PROJECT = "Type"
    # holds the list of subprojects, organized in directories
    # in a project directory
    SUBPROJECTS = "Subprojects"
    # the author of the project, can be faculty or student
    AUTHOR = "Author"

    def __init__(self, name: str, ptype: str, author: Author, subprojects: Optional[List[str]]) -> None:
        if type(name) != str:
            raise TypeError(name)
        self.name = name
        if type(ptype) != str:
            raise TypeError(ptype)
        self.type = ptype
        if type(author) != Author:
            raise TypeError(author)
        self.author = author
        if subprojects != None and subprojects != []:
            self.subprojects = subprojects
        else:
            self.subprojects = []

    def to_dict(self):
        return {
            Project.NAME: self.name,
            Project.TYPE_OF_PROJECT: self.type,
            Project.AUTHOR: self.author.to_dict(),
            Project.SUBPROJECTS: self.subprojects
        }

    def to_yaml(self):
        return yaml.safe_dump(self.to_dict())

    # --- CLI METHODS ---
    # generate projects
    def cli_generate():
        do_create = inquirer.confirm("Do you want to create the project file right now?")
        if do_create:
            # questions to prompt the user
            project_queries = [
                inquirer.Text(
                    'name',
                    'Enter the name of the project'
                ),
                inquirer.List(
                    'type',
                    'Enter the type of project',
                    list(map(lambda x: str(x)[12:].capitalize(), list(ProjectType)))
                )
            ]
            # ask questions and get answers
            answer = inquirer.prompt(project_queries)
            # create an author from CLI prompt
            author: Author = Author.create_author()
            # subprojects list, which is empty presently
            subprojects = []
            spcreateprompt = inquirer.Text(
                'name',
                'Enter the name of the new subproject'
            )
            # add any generated projects here, for each generated project, create
            # an empty directory also
            while True:
                if subprojects == []:
                    if inquirer.confirm("No subprojects created. Create one?"):
                        spname = inquirer.prompt([spcreateprompt])['name']
                        if inquirer.confirm(
                            f"Do you want to continue creating '{spname}'?"
                        ):
                            sp_pathname = os.path.join(os.getcwd(), spname)
                            if not os.path.exists(sp_pathname):
                                os.makedirs(spname)
                            subprojects.append(spname)
                            Subproject.generate_subproject(
                                spname,
                                answer['name'],
                                author.name
                            )
                    else:
                        break
                else:
                    if inquirer.confirm("Do you want to create more projects?"):
                        spname = inquirer.prompt([spcreateprompt])['name']
                        if inquirer.confirm(
                            f"Do you want to continue creating {spname}?"
                        ):
                            os.makedirs(os.path.join(os.getcwd(), spname))
                            subprojects.append(spname)
                            Subproject.generate_subproject(
                                spname, 
                                answer['name'],
                                author.name
                            )
                    else:
                        break
            # return the generated project
            try:
                project_config = Project(answer['name'], answer['type'], author, subprojects)
                with open(os.path.join(os.getcwd(), Project.PROJECT_FILE), 'w') as project_out:
                    project_out.write(project_config.to_yaml())
                    print("Project configuration written")
            except TypeError as te:
                print(te)
                return None
    # manage projects
    @staticmethod
    def cli_manage():
        if not os.path.exists(os.path.join(os.getcwd(), Project.PROJECT_FILE)):
            Project.cli_generate()
        else:
            # if the project file exists:
            #TODO Try to finish this portion of the program too.
            pass


# manage the project
Project.cli_manage()
