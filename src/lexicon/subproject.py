import colorama
import copy
from datetime import datetime
import errno
import inquirer
import os
import pathlib
from typing import Any, Dict, List
import yaml
from yaml.error import YAMLError

from lexicon.commonutils import CLI_VARS_PRETTYPRINT, change_text, check_is_modified
from lexicon.makegenerators import (
    append_lines,
    gen_makefile_module_cmd,
    MAKEFILE_PHONY,
    PHONY_BUILD_ALL,
    PHONY_CLEAN_ALL,
)

from lexicon.module import Module


class Subproject:
    # --- INSTANCE VARIABLES
    name: str
    parent: str
    author: str
    modules: List[Module]

    # --- CLASS VARIABLES
    # - DICT (HASH-MAP) VARIABLES
    NAME = "Name"
    PARENT = "Parent"
    AUTHOR = "Author"
    MODULES = "Modules"
    # - FILENAME
    SUBPROJECT_FILE = "lexicon_sub.yaml"
    LEXICON_SUB_FILE_BACKUP = "." + SUBPROJECT_FILE + ".bkp"

    def __init__(self, args: Dict[str, Any]) -> None:
        # TODO: Argument Validation
        self.name = args[Subproject.NAME].strip()
        self.parent = args[Subproject.PARENT].strip()
        self.author = args[Subproject.AUTHOR]
        self.modules = []
        modules = args[Subproject.MODULES]
        # print(modules)
        for module_name in modules:
            self.modules.append(Module(module_name, modules[module_name]))

    def to_dict(self):
        modules = {}
        for module in self.modules:
            # small modification done here so that to_yaml() can
            # work properly, though that is not really needed for us
            modules[module.name] = module.to_dict()[module.name]
        return {
            Subproject.NAME: self.name,
            Subproject.PARENT: self.parent,
            Subproject.AUTHOR: self.author,
            Subproject.MODULES: modules,
        }

    def to_yaml(self):
        return yaml.safe_dump(self.to_dict())

    def save_config(self, disable_replace=False):
        backup_path = os.path.join(os.getcwd(), Subproject.LEXICON_SUB_FILE_BACKUP)
        subproject_path = os.path.join(os.getcwd(), Subproject.SUBPROJECT_FILE)
        # Backup not implemented, unreachable code for now
        if not disable_replace:
            os.replace(subproject_path, backup_path)
        with open(subproject_path, "w") as new_config_file:
            yaml.safe_dump(self.to_dict(), new_config_file)

    def restore_config():
        backup_path = os.path.join(os.getcwd(), Subproject.LEXICON_SUB_FILE_BACKUP)
        lexicon_path = os.path.join(os.getcwd(), Subproject.SUBPROJECT_FILE)
        if os.path.exists(backup_path):
            os.replace(backup_path, lexicon_path)

    def get_files_not_in_directory(self) -> List[str]:
        files_not_in_dir = []
        for module in self.modules:
            files_not_in_dir += module.get_files_not_in_directory()
        return files_not_in_dir

    def create_files_not_in_directory(self):
        for file in self.get_files_not_in_directory():
            os.mknod(file)

    def create_build_list(self):
        build_modules = []
        for module in self.modules:
            build_modules.append(module.build_command)
        return build_modules

    def create_module_build_list(self):
        build_cmds = map(gen_makefile_module_cmd, self.create_build_list())
        return append_lines(PHONY_BUILD_ALL, *build_cmds)

    def create_clean_list(self):
        clean_modules = []
        for module in self.modules:
            clean_modules.append(module.clean_command)
        return clean_modules

    def create_module_clean_list(self):
        clean_cmds = map(gen_makefile_module_cmd, self.create_clean_list())
        return append_lines(PHONY_CLEAN_ALL, *clean_cmds)

    def create_makefile_overall_lists(self):
        return append_lines(
            MAKEFILE_PHONY, self.create_module_build_list(), self.create_module_clean_list()
        )

    def create_module_recipe_list(self):
        module_recipes = []
        for module in self.modules:
            module_recipes.append(f"# --- MODULE {module.name} ---")
            module_recipes.append(module.gen_complete_make_cmd())
        return append_lines(*module_recipes)

    def generate_makefile(self):
        return append_lines(
            "# MAKEFILE GENERATED BY LEXICON",
            f"# {Subproject.NAME}: {self.name}",
            f"# {Subproject.PARENT}: {self.parent}",
            f"# {Subproject.AUTHOR}: {self.author[:160]}",
            self.create_makefile_overall_lists(),
            self.create_module_recipe_list(),
        ).strip()

    def write_makefile(self, path: str):
        try:
            with open(path, "w") as makefile_obj:
                makefile_obj.write(self.generate_makefile())
            print(colorama.Fore.GREEN + "Makefile Generated." + colorama.Fore.RESET)
        except FileExistsError as fee:
            print(colorama.Fore.RED + "Error in writing Makefile" + colorama.Fore.RESET)
            raise fee
        except OSError as ose:
            print(colorama.Fore.RED + "Error in writing Makefile" + colorama.Fore.RESET)
            raise ose

    # subroutine to generate a subproject
    @staticmethod
    def generate_subproject(subproject_name: str, parent_name: str, author: str):
        os.chdir(os.path.join(os.getcwd(), subproject_name))
        if os.path.exists(os.path.join(os.getcwd(), "lexicon_sub.yaml")):
            if inquirer.confirm("A project file exists here. Create a new one?"):
                Subproject(
                    {
                        Subproject.NAME: subproject_name,
                        Subproject.PARENT: parent_name,
                        Subproject.AUTHOR: author,
                        Subproject.MODULES: [],
                    }
                ).save_config(disable_replace=True)
        else:
            Subproject(
                {
                    Subproject.NAME: subproject_name,
                    Subproject.PARENT: parent_name,
                    Subproject.AUTHOR: author,
                    Subproject.MODULES: [],
                }
            ).save_config(disable_replace=True)
        Subproject.cli_manage()
        os.chdir(pathlib.Path(*pathlib.Path(os.getcwd()).parts[:-1]))

    @staticmethod
    def transfer_control(subproject_name: str, is_check_needed: bool = True):
        # check if we are in a project directory
        if os.path.exists(os.path.join(os.getcwd(), "lexicon.yaml")) or not is_check_needed:
            # we are in a project directory
            try:
                ans = None
                # change to the subproject directory
                os.chdir(os.path.join(os.getcwd(), subproject_name))
                # if the subproject file exists
                if os.path.exists(os.path.join(os.getcwd(), "lexicon_sub.yaml")):
                    # manage the project
                    ans = Subproject.cli_manage()
                    # get back to the project directory
                else:
                    # error that the subproject file can't be found
                    print(
                        colorama.Fore.RED
                        + "Project configuration file doesn't exist."
                        + colorama.Fore.RESET
                    )
                # go back to the parent directory
                # TODO: USE FIND AND REIMPLEMENT ALL PLACES OF PATH MANIPULATION USING PATHLIB
                os.chdir(pathlib.Path(*pathlib.Path(os.getcwd()).parts[:-1]))
                print(os.getcwd())
                return ans
            except OSError as ose:
                raise ose

    # -- VARIABLES FOR THE STATIC METHOD
    CHOICE = "choice"

    # CLI Management
    @staticmethod
    def cli_manage():
        # root prompt for 'Subproject'
        sub_filepath = os.path.join(os.getcwd(), Subproject.SUBPROJECT_FILE)
        if not os.path.exists(sub_filepath):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), sub_filepath)
        try:
            subproject_config = yaml.safe_load(open(sub_filepath, "r"))
            subproject_config: "Subproject" = Subproject(subproject_config)
            reset_subconfig = copy.deepcopy(subproject_config)
            is_modified = False
            # CLI Loop
            while True:
                # ROOT PROMPT
                root_prompt = inquirer.List(
                    Subproject.CHOICE,
                    message=f"""Manage {
                        colorama.Fore.YELLOW
                    }Subproject {colorama.Fore.BLUE}{subproject_config.name} {
                        check_is_modified(is_modified,f'{colorama.Fore.GREEN}<modified>')
                    }{colorama.Fore.RESET}""",
                    choices=[
                        "Modify Properties",
                        "Manage Modules",
                        "Verify",
                        "Reset",
                        "Generate Makefile",
                        "Exit",
                    ],
                )
                choice = inquirer.prompt([root_prompt])[Module.CHOICE]
                # ALL CHOICES ARE SELECTED HERE
                # If we're exiting it, make sure we do it properly.
                if choice == "Exit":
                    if is_modified:
                        modify_write = inquirer.confirm(
                            "Subproject has been changed. Do you want to save changes?"
                        )
                        if modify_write:
                            subproject_config.save_config()
                    return is_modified
                elif choice == "Generate Makefile":
                    # THESE ARE THE SUBROUTINES NECESSARY TO GENERATE MAKEFILES PROPERLY
                    makefile_path = os.path.join(os.path.dirname(sub_filepath), "Makefile")
                    # check if makefile exists
                    if os.path.exists(makefile_path):
                        # if so, create backup if needed
                        backup_confirmation = inquirer.confirm(
                            "Do you want to create a backup of your Makefile?"
                        )
                        if backup_confirmation:
                            backup_makefile_path = os.path.join(
                                os.path.dirname(sub_filepath),
                                "backups",
                                "Makefile_" + datetime.isoformat(datetime.now()) + ".bkp",
                            )
                            if not os.path.exists(os.path.dirname(backup_makefile_path)):
                                os.makedirs(os.path.dirname(backup_makefile_path))
                            os.replace(makefile_path, backup_makefile_path)
                        else:
                            os.remove(makefile_path)
                    subproject_config.write_makefile(makefile_path)
                elif choice == "Manage Modules":
                    while True:
                        module_map = {}
                        for module in subproject_config.modules:
                            module_map[module.name] = copy.deepcopy(module)
                        module_list = list(module_map.keys()) + ["Create a module", "Exit"]
                        module_prompt = inquirer.List(
                            "module_choice", "Select a module or an action", choices=module_list
                        )
                        module_choice = inquirer.prompt([module_prompt])["module_choice"]
                        if module_choice == "Exit":
                            break
                        elif module_choice == "Create a module":
                            module = Module.generate_module(
                                subproject_config.name, subproject_config.parent
                            )
                            subproject_config.modules.append(module)
                            is_modified = True
                        else:
                            selected_module: Module = module_map[module_choice]
                            selected_module_index = None
                            i = 0
                            for module in subproject_config.modules:
                                if selected_module.name == module.name:
                                    selected_module_index = i
                                i += 1
                            is_module_modified, result = Module.cli_manage(
                                selected_module, subproject_config.name, subproject_config.parent
                            )
                            if is_module_modified:
                                subproject_config.modules[selected_module_index] = result
                                is_modified = True
                                print(
                                    f"""Modifications to {
                                    colorama.Fore.BLUE
                                }{selected_module.name}{colorama.Fore.RESET} applied to {
                                    colorama.Fore.YELLOW
                                }{subproject_config.name}{colorama.Fore.RESET}"""
                                )
                elif choice == "Verify":
                    is_verified = None
                    files_not_in_dirs = []
                    for module in subproject_config.modules:
                        if module.verify():
                            if is_verified is not False:
                                is_verified = True
                        else:
                            files_not_in_dirs += module.get_files_not_in_directory()
                            is_verified = False
                    if is_verified:
                        print(
                            f"""{colorama.Fore.GREEN}The subproject {
                            subproject_config.name
                        } has no errors.{colorama.Fore.RESET}"""
                        )
                    else:
                        print(
                            f"""{colorama.Fore.RED}The subproject {
                            subproject_config.name
                        } has errors.{colorama.Fore.RESET}"""
                        )
                elif choice == "Reset":
                    reset_confirm = inquirer.confirm(
                        "Do you want to reset the subproject configuration?"
                    )
                    if reset_confirm:
                        subproject_config = reset_subconfig
                        is_modified = False
                elif choice == "Modify Properties":
                    subproject_dict = subproject_config.to_dict()
                    keydictionary = {}
                    for var in [Subproject.NAME, Subproject.PARENT, Subproject.AUTHOR]:
                        keydictionary[CLI_VARS_PRETTYPRINT.format(var, subproject_dict[var])] = var
                    choice_list = inquirer.List(
                        "subproject_key",
                        message="Select the property to modify",
                        choices=list(keydictionary.keys()),
                    )
                    choice_property = keydictionary[
                        inquirer.prompt([choice_list])["subproject_key"]
                    ]
                    result, answer = change_text(choice_property, subproject_dict[choice_property])
                    if result:
                        if choice_property == Subproject.NAME:
                            subproject_config.name = answer
                        elif choice_property == Subproject.PARENT:
                            subproject_config.parent = answer
                        elif choice_property == Subproject.AUTHOR:
                            subproject_config.author = answer
                        is_modified = True
        except YAMLError as ye:
            raise ye
        except OSError as ose:
            raise ose
