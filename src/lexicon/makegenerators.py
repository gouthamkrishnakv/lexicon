from typing import List

MAKEFILE_PHONY = ".PHONY: all clean"
PHONY_BUILD_ALL = "all:"
PHONY_CLEAN_ALL = "clean:"

COMPILE_COMMAND: str = "\tiverilog -o $@ $^"
CLEAN_COMMAND: str = "\t-rm $({}) $({})"
EXECUTABLE_COMMAND: str = "\ttimeout {}s vvp $<"
EXECUTABLE_WITHOUT_TIMEOUT_COMMAND = "vvp $<"
REPORT_COMMAND: str = '\t@printf "\\e[0;94m{}\\e[0m\\n"'
VIEWER_COMMAND: str = "\tgtkwave -6 $<"
MAKEFILE_MODULE_COMMAND: str = "\tmake {}"

CONST_INPUT_COMMAND: str = "{}:\t$({})"
INPUT_OUTPUT_COMMAND: str = "$({}):\t$({})"


def gen_executable(timeout_in_seconds: int = 10):
    if timeout_in_seconds <= 0:
        return EXECUTABLE_WITHOUT_TIMEOUT_COMMAND
    else:
        return EXECUTABLE_COMMAND.format(str(timeout_in_seconds))


def gen_report(outstring: str = ""):
    return REPORT_COMMAND.format(outstring)


def gen_inputvar_const(inputvar: str = "", constvar: str = ""):
    return CONST_INPUT_COMMAND.format(constvar, inputvar)


def gen_input_output(inputvar: str = "", outputvar: str = ""):
    return INPUT_OUTPUT_COMMAND.format(outputvar, inputvar)


def gen_report_cmd(mod_name: str = "", message: str = ""):
    return REPORT_COMMAND.format(f"{mod_name}: \\e[0;92m{message}")


def gen_makefile_module_cmd(module_name: str):
    return MAKEFILE_MODULE_COMMAND.format(module_name)


def append_lines(*commands: List[str]) -> str:
    final_output = ""
    for command in commands:
        final_output += command + "\n"
    return final_output
