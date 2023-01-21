#!/usr/bin/python3
# This holds the information regarding the students for the project needed.

import os
from copy import deepcopy
from enum import Enum
from typing import Any, Dict, List

import colorama
import inquirer
import yaml

from lexicon.author import Author, AuthorType
from lexicon.commonutils import (CLI_VARS_PRETTYPRINT, change_text,
                                 check_is_modified)
from lexicon.subproject import Subproject


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
    subprojects: List[str]

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

    def __init__(self, args: Dict[str, Any]) -> None:
        self.name = args[Project.NAME].strip()
        self.type = ProjectType(args[Project.TYPE_OF_PROJECT].strip())
        author = args[Project.AUTHOR]
        self.author = Author(AuthorType(author[Author.TYPE].lower()), author[Author.NAME])
        self.subprojects = args[Project.SUBPROJECTS]

    def to_dict(self):
        return {
            Project.NAME: self.name,
            Project.TYPE_OF_PROJECT: self.type.value,
            Project.AUTHOR: self.author.to_dict(),
            Project.SUBPROJECTS: self.subprojects,
        }

    def to_yaml(self):
        return yaml.safe_dump(self.to_dict())

    def save_config(self):
        project_path = os.path.join(os.getcwd(), Project.PROJECT_FILE)
        with open(project_path, "w") as new_config_file:
            yaml.safe_dump(self.to_dict(), new_config_file)

    # --- CLI METHODS ---
    # generate projects
    def cli_generate():
        do_create = inquirer.confirm("Do you want to create the project file right now?")
        if do_create:
            # questions to prompt the user
            project_queries = [
                inquirer.Text("name", "Enter the name of the project"),
                inquirer.List("type", "Enter the type of project", [e.value for e in ProjectType]),
            ]
            # ask questions and get answers
            answer = inquirer.prompt(project_queries)
            # create an author from CLI prompt
            author: Author = Author.create_author()
            # subprojects list, which is empty presently
            subprojects = []
            spcreateprompt = inquirer.Text("name", "Enter the name of the new subproject")
            # add any generated projects here, for each generated project, create
            # an empty directory also
            while True:
                if subprojects == []:
                    if inquirer.confirm("No subprojects created. Create one?"):
                        spname = inquirer.prompt([spcreateprompt])["name"]
                        if inquirer.confirm(f"Do you want to continue creating '{spname}'?"):
                            sp_pathname = os.path.join(os.getcwd(), spname)
                            if not os.path.exists(sp_pathname):
                                os.makedirs(spname)
                            subprojects.append(spname)
                            Subproject.generate_subproject(spname, answer["name"], author.name)
                    else:
                        break
                else:
                    if inquirer.confirm("Do you want to create more subprojects?"):
                        spname = inquirer.prompt([spcreateprompt])["name"]
                        if inquirer.confirm(f"Do you want to continue creating {spname}?"):
                            os.makedirs(os.path.join(os.getcwd(), spname))
                            subprojects.append(spname)
                            Subproject.generate_subproject(spname, answer["name"], author.name)
                    else:
                        break
            # return the generated project
            try:
                project_config = Project(
                    {
                        Project.AUTHOR: author.to_dict(),
                        Project.NAME: spname,
                        Project.TYPE_OF_PROJECT: answer["type"],
                        Project.SUBPROJECTS: subprojects,
                    }
                )
                print(project_config.to_yaml())
                with open(os.path.join(os.getcwd(), Project.PROJECT_FILE), "w") as project_out:
                    project_out.write(project_config.to_yaml())
                    print("Project configuration written")
            except TypeError as te:
                print(te)
                return None

    # --  VARIABLES FOR STATIC METHOD --
    CHOICE = "choice"

    # manage projects
    @staticmethod
    def cli_manage():
        project_path = os.path.join(os.getcwd(), Project.PROJECT_FILE)
        if not os.path.exists(project_path):
            Project.cli_generate()
        else:
            project_config = yaml.safe_load(open(project_path, "r"))
            project_config: "Project" = Project(project_config)
            print(project_config.to_dict())
            current_config = deepcopy(project_config)
            is_modified = False
            # CLI Loop
            while True:
                root_prompt = inquirer.List(
                    Project.CHOICE,
                    message=f"""Manage {
                            colorama.Fore.YELLOW
                        }Project {colorama.Fore.BLUE}{project_config.name} {
                            check_is_modified(is_modified, f'{colorama.Fore.GREEN}<modified>')
                        }{colorama.Fore.RESET}""",
                    choices=[
                        "Manage Subprojects",
                        "Modify Properties",
                        "Reset",
                        "View Configuration",
                        "Exit",
                    ],
                )
                try:
                    choice = inquirer.prompt([root_prompt])[Project.CHOICE]
                except TypeError:
                    continue
                if choice is None:
                    continue
                elif choice == "Exit":
                    if is_modified:
                        modify_write = inquirer.confirm(
                            "Project has been modified. Do you want to save changes?"
                        )
                        print(f"UMODIFIED:{current_config.to_dict()}")
                        print(f"MODIFIED: {project_config.to_dict()}")
                        if modify_write:
                            project_config.save_config()
                            print(
                                f"""{
                                    colorama.Fore.GREEN
                                } Configuration file saved in filepath {colorama.Fore.YELLOW}{
                                    os.path.join(os.getcwd(), Project.PROJECT_FILE)
                                }{colorama.Fore.RESET} ."""
                            )
                    break
                elif choice == "Reset":
                    project_config = deepcopy(current_config)
                    is_modified = False
                elif choice == "Manage Subprojects":
                    # SUBPROJECT LOOP
                    while True:
                        subproject_choices = list(project_config.subprojects) + [
                            "Create a subproject",
                            "Exit",
                        ]
                        subproject_prompt = inquirer.List(
                            "subproject_choice",
                            "Select Subproject to manage",
                            choices=subproject_choices,
                        )
                        subproject_choice = inquirer.prompt([subproject_prompt])[
                            "subproject_choice"
                        ]
                        if subproject_choice == "Exit":
                            break
                        elif subproject_choice == "Create a subproject":
                            # USE Subproject.generate_subproject to create a subproject here
                            # and add it to project_config.subprojects
                            spcreateprompt = inquirer.Text(
                                "subproject_name", "Enter the name for the subproject"
                            )
                            spname = inquirer.prompt([spcreateprompt])
                            if spname is not None:
                                spname = spname["subproject_name"]
                                if spname.strip() != "":
                                    os.makedirs(os.path.join(os.getcwd(), spname))
                                    project_config.subprojects.append(spname)
                                    Subproject.generate_subproject(
                                        spname, project_config.name, project_config.author.name
                                    )
                                    is_modified = True
                                else:
                                    print(
                                        f"""{
                                            colorama.Fore.RED
                                        } NO NAME GIVEN. IGNORING.{
                                            colorama.Fore.RESET
                                        }"""
                                    )
                                    break
                            else:
                                break
                        else:
                            subproject_name = subproject_choice
                            print(
                                f"""{
                                    colorama.Fore.BLUE
                                }Switching to subproject {colorama.Fore.YELLOW}{
                                    subproject_choice
                                }{colorama.Fore.RESET}"""
                            )
                            subproject_path = os.path.join(
                                os.path.dirname(project_path), subproject_name
                            )
                            print(subproject_path)
                            if os.path.exists(subproject_path):
                                sub_is_modified = Subproject.transfer_control(subproject_name)
                                if sub_is_modified:
                                    is_modified = True
                            else:
                                print(
                                    f"""{
                                        colorama.Fore.RED
                                    }PATH DOES NOT EXIST{
                                        colorama.Fore.RESET
                                    }"""
                                )
                                break
                elif choice == "Modify Properties":
                    # Choice for Project Properties
                    project_dict = project_config.to_dict()
                    keydictionary = {}
                    for var in [
                        Project.NAME,
                        Project.TYPE_OF_PROJECT,
                        # Project.AUTHOR
                    ]:
                        keydictionary[CLI_VARS_PRETTYPRINT.format(var, project_dict[var])] = var
                    keydictionary[
                        CLI_VARS_PRETTYPRINT.format(
                            Project.AUTHOR, project_dict[Project.AUTHOR][Author.NAME]
                        )
                    ] = Project.AUTHOR
                    choice_list = inquirer.List(
                        "project_key",
                        message="Select the property to modify",
                        choices=list(keydictionary.keys()),
                    )
                    try:
                        choice_property = keydictionary[
                            inquirer.prompt([choice_list])["project_key"]
                        ]
                    except TypeError:
                        continue
                    if choice_property is None:
                        continue
                    elif choice_property == Project.NAME:
                        result, answer = change_text(choice_property, project_dict[choice_property])
                        if result:
                            project_config.name = answer
                        else:
                            break
                    elif choice_property == Project.TYPE_OF_PROJECT:
                        # let user select the type of project the user needs
                        type_choices_prompt = inquirer.List(
                            "project_type",
                            "Select the property type you want to switch to",
                            choices=[ptype.value for ptype in ProjectType],
                            default=project_config.type,
                        )
                        try:
                            ptype_choice = inquirer.prompt([type_choices_prompt])["project_type"]
                            # project type changed here
                            project_config.type = ProjectType(ptype_choice)
                        except TypeError:
                            continue
                    elif choice_property == Project.AUTHOR:
                        # This is a difficult part of code, there's multiple exchange of
                        # key-value pairs, make sure to print 'keydictionary' and understand
                        # how it works.
                        author = project_config.author
                        author_dict = author.to_dict()
                        keydictionary = {}
                        keydictionary[
                            CLI_VARS_PRETTYPRINT.format(Author.NAME, author.name)
                        ] = Author.NAME
                        keydictionary[
                            CLI_VARS_PRETTYPRINT.format(Author.TYPE, author.type.value)
                        ] = Author.TYPE
                        # Select the author
                        author_choices_prompt = inquirer.List(
                            "author_prop",
                            "Select the property to modify",
                            choices=list(keydictionary.keys()),
                        )
                        answer = None
                        try:
                            answer = keydictionary[
                                inquirer.prompt([author_choices_prompt])["author_prop"]
                            ]
                        except KeyError:
                            continue
                        print(answer)
                        if answer is None:
                            continue
                        elif answer == Author.NAME:
                            result, answer = change_text(answer, author_dict[answer])
                            if result:
                                author.name = answer
                        elif answer == Author.TYPE:
                            author_type_choices = inquirer.List(
                                "author_type",
                                "Select the type of author to be changed to",
                                choices=[atype.value for atype in AuthorType],
                            )
                            try:
                                new_author_type = AuthorType(
                                    inquirer.prompt([author_type_choices])["author_type"]
                                )
                            except KeyError:
                                continue
                            author.type = new_author_type
                        project_config.author = author
                    is_modified = True
                elif choice == "View Configuration":
                    print(
                        f"{colorama.Fore.YELLOW}"
                        f"Configuration from "
                        f"{colorama.Fore.GREEN}{project_path}{colorama.Fore.RESET}"
                    )
                    print(f"{colorama.Fore.BLUE}-- START OF CONFIGURATION --{colorama.Fore.RESET}")
                    print(project_config.to_yaml())
                    print(f"{colorama.Fore.BLUE}-- END OF CONFIGURATION --{colorama.Fore.RESET}")
