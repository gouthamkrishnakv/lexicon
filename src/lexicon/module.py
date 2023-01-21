import copy
import glob
import os
from typing import Any, Dict, List, Tuple

import colorama
import inquirer
import yaml

from lexicon.commonutils import (CLI_VARS_PRETTYPRINT, change_text,
                                 check_is_modified)
from lexicon.filegenerators import generate_quickstart_template
from lexicon.makegenerators import (CLEAN_COMMAND, COMPILE_COMMAND,
                                    VIEWER_COMMAND, append_lines,
                                    gen_executable, gen_input_output,
                                    gen_inputvar_const, gen_report_cmd)


def remove_files_in_directory(files: List[str], extension: str = "*.v"):
    dirfiles = glob.glob(extension, recursive=False)
    for file in dirfiles:
        if file in files:
            files.remove(file)
    return files


# +------------------------------------------------------------------------+
# |TODO: CHANGE ALL THE ASSERTIONS TO CONDITIONAL ValueError Exceptions....|
# +------------------------------------------------------------------------+
class Module:
    # --- CLASS MEMBERS (INSTANCE VARIABLES) ---
    # module name
    name: str
    # module file
    files: List[str]
    files_var: str
    # module executable
    exec_file: str
    exec_filevar: str
    # module wave files (with '.vcd' extension)
    wave_file: str
    wave_filevar: str
    # build command
    build_command: str
    # clean command
    clean_command: str
    # exec command
    exec_command: str
    # timeout for the executable
    timeout: int

    # --- CLASS VARIABLES ---
    # - CONSTANTS NEEDED FOR HASH-MAP RESOLUTION
    FILES = "files"
    FILES_VAR = "files_var"
    EXEC = "exec"
    EXEC_VAR = "exec_var"
    WAVE = "wave"
    WAVE_VAR = "wave_var"
    BUILD_COMMAND = "build_command"
    CLEAN_COMMAND = "clean_command"
    EXEC_COMMAND = "exec_command"
    TIMEOUT = "timeout"
    # - ERROR MESSAGES
    STR_ERR = "{} of {} must be a string"
    FILE_ERR = "{} of {} must be a list of files (as strings)"
    VARIABLE_ERR = "variable '{}' ({}) in {} MUST NOT have spaces"
    # DEFAULT VARIABLES
    # TODO: Move this to a user/project configuration file when needed.
    # default timeout: 10 seconds
    DEFAULT_TIMEOUT = 10

    # --- METHODS ---
    # constructor for a specific module
    def __init__(self, name: str, args: Dict[str, Any]) -> None:
        # name
        name = name.strip()
        if " " in name:
            raise ValueError(
                f"Change the name of module '{name}' so it doesn't have any spaces in it."
            )
        if name != name.lower():
            raise ValueError(f"The module '{name}' must not contain capital letters. Change it.")
        self.name = name
        # files
        if args is None:
            args = {}
        if Module.FILES in args:
            if args[Module.FILES] is None:
                self.files = []
            if type(args[Module.FILES]) != list:
                print(args[Module.FILES])
                raise ValueError(Module.FILE_ERR.format(Module.FILES, self.name))
            for file in args[Module.FILES]:
                if type(file) != str:
                    raise ValueError(f"invalid filename '{file}' for {self.name}")
            self.files = args[Module.FILES]
        else:
            testbench_file: str = f"{self.name}_tb.v"
            module_file: str = f"{self.name}_mod.v"
            tempfiles = [testbench_file, module_file]
            print("Keys not given.")
            print("Defaulting to modules " + str(tempfiles))
            self.files = tempfiles
        # files_var
        if Module.FILES_VAR in args:
            # validation
            if type(args[Module.FILES_VAR]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.files_var, self.files_var))
            if " " in args[Module.FILES_VAR]:
                raise ValueError(
                    Module.VARIABLE_ERR.format(args[Module.FILES_VAR], Module.files_var)
                )
            self.files_var = args[Module.FILES_VAR]
        else:
            self.files_var = self.name.upper() + "_FILES"
        # exec
        if Module.EXEC in args:
            # validation
            if type(args[Module.EXEC]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.EXEC, self.name))
            self.exec_file = args[Module.EXEC]
        else:
            self.exec_file = self.name + ".vvp"
        # exec_var
        if Module.EXEC_VAR in args:
            # validation
            if type(Module.EXEC_VAR) is not str:
                raise ValueError(Module.STR_ERR.format(Module.EXEC_VAR, self.name))
            self.exec_filevar = args[Module.EXEC_VAR]
        else:
            self.exec_filevar = self.name.upper() + "_EXEC"
        # exec command
        if Module.EXEC_COMMAND in args:
            # validation
            if type(args[Module.EXEC_COMMAND]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.EXEC_COMMAND, self.name))
            self.exec_command = args[Module.EXEC_COMMAND]
        else:
            self.exec_command = self.name + "_exec"
        # wave
        if Module.WAVE in args:
            # validation
            if type(args[Module.WAVE]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.WAVE, self.name))
            self.wave_file = args[Module.WAVE]
        else:
            self.wave_file = self.name + ".vcd"
        # wave_var
        if Module.WAVE_VAR in args:
            # Validation
            if type(args[Module.WAVE_VAR]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.WAVE_VAR, self.name))
            self.wave_filevar = args[Module.WAVE_VAR]
        else:
            self.wave_filevar = self.name.upper() + "_WAVE"
        # build command
        if Module.BUILD_COMMAND in args:
            # validation
            if type(args[Module.BUILD_COMMAND]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.BUILD_COMMAND, self.name))
            self.build_command = args[Module.BUILD_COMMAND]
        else:
            # use the module name itself for build
            self.build_command = self.name.lower()
        # clean command
        if Module.CLEAN_COMMAND in args:
            # validation
            if type(args[Module.CLEAN_COMMAND]) is not str:
                raise ValueError(Module.STR_ERR.format(Module.BUILD_COMMAND, self.name))
            self.clean_command = args[Module.CLEAN_COMMAND]
        else:
            # name + "_clean" for the clean job in makefile
            self.clean_command = self.name + "_clean"
        # timeout
        if Module.TIMEOUT in args:
            # validation
            if type(args[Module.TIMEOUT]) is not int:
                raise ValueError(f"timeout of {self.name} must be an integer")
            try:
                self.timeout = int(args[Module.TIMEOUT])
            except Exception as e:
                raise e
        else:
            self.timeout = Module.DEFAULT_TIMEOUT

    # generate a dictionary (hash-map) object for representation
    def to_dict(self):
        return {
            self.name: {
                Module.FILES: self.files,
                Module.FILES_VAR: self.files_var,
                Module.EXEC: self.exec_file,
                Module.EXEC_VAR: self.exec_filevar,
                Module.WAVE: self.wave_file,
                Module.WAVE_VAR: self.wave_filevar,
                Module.BUILD_COMMAND: self.build_command,
                Module.EXEC_COMMAND: self.exec_command,
                Module.CLEAN_COMMAND: self.clean_command,
                Module.TIMEOUT: self.timeout,
            }
        }

    # generate yaml file back
    def to_yaml(self):
        return yaml.safe_dump(self.to_dict())

    def verify(self):
        return remove_files_in_directory(self.files) == []

    def create_files_not_in_directory(self):
        for file in self.get_files_not_in_directory():
            os.mknod(file)

    def get_files_not_in_directory(self):
        return remove_files_in_directory(self.files, "*.v")

    # --- GENERATION METHODS

    # A FILE VARIABLE GENERATION
    #     - exec file generation
    def gen_exec_file(self):
        return f"{self.exec_filevar} = {self.exec_file}"

    #     - wave file generation
    def gen_wave_file(self):
        return f"{self.wave_filevar} = {self.wave_file}"

    #     - files variable generation
    def gen_files_var(self):
        comment = f"# {self.name}: VARS"
        files_var = f"{self.files_var} ="
        for file in self.files:
            files_var += " " + file
        return comment + "\n" + files_var

    # a OVERALL FILE DEFENITION GENERATION
    def gen_file_cmd(self):
        return append_lines(self.gen_files_var(), self.gen_exec_file(), self.gen_wave_file())

    # B BUILD PROCESS GENERATION
    #   - compile process generation
    def gen_compile_cmd(self):
        return append_lines(
            f"# {self.name}: BUILD -> COMPILE",
            gen_input_output(self.files_var, self.exec_filevar),
            gen_report_cmd(self.name, "Compiling Source Files..."),
            COMPILE_COMMAND,
        )

    #   - execute command generation
    def gen_execute_cmd(self):
        return append_lines(
            f"# {self.name}: BUILD -> EXECUTE",
            f"# '{self.exec_command}' target",
            gen_inputvar_const(self.wave_filevar, self.exec_command),
            gen_report_cmd(self.name, f"Execution Target '{self.exec_command}' reached"),
            "",
            f"# {self.name}: Execute {self.exec_filevar}",
            gen_input_output(self.exec_filevar, self.wave_filevar),
            gen_report_cmd(self.name, f"Running Simulation with timeout \\e[1;93m{self.timeout}s"),
            gen_executable(self.timeout),
        )

    #   - view command generation
    def gen_viewer_cmd(self):
        return append_lines(
            f"# {self.name}: BUILD -> VIEW",
            gen_inputvar_const(self.wave_filevar, self.build_command),
            gen_report_cmd(self.name, "Running Simulation"),
            VIEWER_COMMAND,
        )

    # b - whole build + execute process
    def gen_view_cmd(self):
        return append_lines(
            f"# {self.name}: BUILD",
            self.gen_viewer_cmd(),
            self.gen_execute_cmd(),
            self.gen_compile_cmd(),
        )

    # B CLEAN PROCESS GENERATION
    def gen_clean_cmd(self):
        return append_lines(
            f"# {self.name}: CLEAN",
            f"{self.clean_command}:",
            gen_report_cmd(self.name, "Cleaning files of the module"),
            CLEAN_COMMAND.format(self.exec_filevar, self.wave_filevar),
        )

    def gen_complete_make_cmd(self):
        return append_lines(self.gen_file_cmd(), self.gen_view_cmd(), self.gen_clean_cmd())

    # --- VARIABLES FOR THE STATIC METHOD
    CHOICE = "choice"

    # --- CLI METHODS ---
    def generate_module(subproject_name: str, parent_name: str):
        module_prompt = inquirer.Text("modname", "Enter the name of the new module")
        modname = inquirer.prompt([module_prompt])["modname"]
        if modname is None:
            raise TypeError(modname)
        else:
            new_module = Module(modname, None)
            new_module.create_files_not_in_directory()
            new_module.cli_manage(new_module, subproject_name, parent_name)
            return new_module

    #   - CLI specific variables
    CLI_VARS_PRETTYPRINT: str = (
        colorama.Fore.BLUE + "{}: " + colorama.Fore.YELLOW + "{}" + colorama.Fore.RESET
    )

    def get_vars_prettyprint(choice: str):
        values = choice.split(":")
        return (values[0].strip(), values[1].strip())

    @staticmethod
    def cli_manage(
        module: "Module", subproject_name: str, project_name: str
    ) -> Tuple[bool, "Module"]:
        reset_module = copy.deepcopy(module)
        is_modified = False
        if module.files == []:
            generate_res = inquirer.confirm(
                "Module files are empty. Do you want to generate default module files?"
            )
            if generate_res:
                module.files = generate_quickstart_template(module, subproject_name, project_name)
                is_modified = True
        if module is None:
            # TODO: add a conditional module generator here
            raise TypeError(module)
        if subproject_name is None:
            raise UserWarning("Subproject name is not given")
        if project_name is None:
            raise UserWarning("Project name is not given")
        while True:
            root_prompt = inquirer.List(
                Module.CHOICE,
                message=f"""Manage Module {colorama.Fore.BLUE}{module.name} {check_is_modified(
                        is_modified,
                        f'{colorama.Fore.GREEN}<modified>'
                    )}{colorama.Fore.RESET}""",
                choices=["Modify Properties", "Add or Remove Files", "Reset", "Verify", "Exit"]
            )
            # print(module.to_yaml())
            # ASK THE QUESTION
            choice = inquirer.prompt([root_prompt])[Module.CHOICE]
            # IF THE ANSWER IS EXIT
            if choice.strip() == "Exit":
                return (is_modified, module)
            # IF THE ANSWER IS TO ADD OR REMOVE FILES
            elif choice == "Add or Remove Files":
                # print("FILES IN DIR: " + str(glob.glob("*.v")))
                # print("FILES IN MODULE: " + str(module.files))
                file_select_inquiry = [
                    inquirer.Checkbox(
                        "files",
                        message="Select the files needed for selection"
                        "(use space bar to select or deselect an object)",
                        choices=glob.glob("*.v", recursive=False),
                        default=module.files,
                    )
                ]
                response = inquirer.prompt(file_select_inquiry)["files"]
                # print("FILES AFTER RESPONSE: " + str(response))
                # print("FILES IN MODULE AFTER RESPONSE: " + str(module.files))
                if response != module.files:
                    module.files = response
                    is_modified = True
            # IF WE NEED TO RESET THE VARIABLES
            elif choice == "Reset":
                reset_prompt = inquirer.confirm("Do you want to discard all changes?")
                if reset_prompt:
                    module = copy.deepcopy(reset_module)
                    is_modified = False
            # IF WE NEED TO VERIFY THE RESOURCES
            elif choice == "Verify":
                if module.get_files_not_in_directory() == []:
                    print(
                        colorama.Fore.GREEN
                        + "Module is verified to not have any problems."
                        + colorama.Fore.RESET
                    )
                else:
                    print(
                        colorama.Fore.RED
                        + "The module has some files which do not yet exist."
                        + colorama.Fore.RESET
                    )
                    print(f"Files not in directory: {module.get_files_not_in_directory()}")
                    do_reset = inquirer.confirm("Do you want to generate these files?")
                    if do_reset:
                        module.create_files_not_in_directory()
                        print(
                            "All files for '"
                            f"{colorama.Fore.BLUE}{module.name}{colorama.Fore.RESET}"
                            "' created."
                        )
            elif choice == "Modify Properties":
                module_dict = module.to_dict()[module.name]
                keydictionary = {}
                for var in [
                    Module.FILES_VAR,
                    Module.EXEC,
                    Module.EXEC_VAR,
                    Module.WAVE,
                    Module.WAVE_VAR,
                    Module.BUILD_COMMAND,
                    Module.CLEAN_COMMAND,
                    Module.TIMEOUT,
                ]:
                    keydictionary[CLI_VARS_PRETTYPRINT.format(var, module_dict[var])] = var
                choice_list = inquirer.List(
                    "module_key",
                    message="Select the property to change",
                    choices=list(keydictionary.keys()),
                )
                choice_property = keydictionary[inquirer.prompt([choice_list])["module_key"]]
                result, answer = change_text(choice_property, module_dict[choice_property])
                if result:
                    if choice_property == Module.FILES_VAR:
                        module.files_var = answer
                    elif choice_property == Module.EXEC:
                        module.exec_file = answer
                    elif choice_property == Module.EXEC_VAR:
                        module.exec_filevar = answer
                    elif choice_property == Module.WAVE:
                        module.wave_file = answer
                    elif choice_property == Module.WAVE_VAR:
                        module.wave_filevar = answer
                    elif choice_property == Module.BUILD_COMMAND:
                        module.build_command = answer
                    elif choice_property == Module.CLEAN_COMMAND:
                        module.clean_command = answer
                    elif choice_property == Module.TIMEOUT:
                        module.timeout = int(answer)
                    is_modified = True
