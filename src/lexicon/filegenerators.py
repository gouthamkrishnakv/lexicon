from glob import glob
import os
import pathlib
from string import Template
from typing import Any


def create_template(var: str, module: Any, subproject: str, project: str) -> str:
    return Template(var).safe_substitute(
        name=module.name,
        exec=module.exec_file,
        wave=module.wave_file,
        buildcommand=module.build_command,
        cleancommand=module.clean_command,
        subproject=subproject,
        project=project,
    )


def generate_quickstart_template(module: Any, subproject: str, project: str) -> list[str]:
    templates = glob(pathlib.Path(pathlib.Path(os.getcwd()).parts[:-1]), "*.v.lexicon_qs")
    generated_files = []
    for file in templates:
        new_filename = create_template(file, module, subproject, project)[:-11]
        generated_files.append(new_filename)
        with open(file, "r") as infile:
            with open(new_filename, "w") as outfile:
                outfile.write(create_template(infile.read(), module, subproject, project))
    return generated_files


# generate_template(newmod, "A1Q01", "Assignment_01")
