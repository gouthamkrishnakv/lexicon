from re import match
from typing import Tuple
import inquirer
import colorama


def change_text(property: str, value: str) -> Tuple[bool, str]:
    text_modify_question = inquirer.Text(
        name="property",
        message=f"Modify {colorama.Fore.BLUE}{property}{colorama.Fore.RESET}",
        default=value,
    )
    answer = inquirer.prompt([text_modify_question])["property"].strip()
    if inquirer.confirm(
        f"Are you sure you want to change {colorama.Fore.BLUE}{property}{colorama.Fore.RESET} to {colorama.Fore.YELLOW}{answer}{colorama.Fore.RESET}?"  # noqa: E501
    ):
        return (True, answer)
    return (False, None)


def change_int(property: str, value: int) -> Tuple[bool, int]:
    int_modify_question = inquirer.Text(
        name="property",
        message=f"Modify {colorama.Fore.BLUE}{property}{colorama.Fore.RESET}",
        default=value,
        validate=lambda _, x: match("^\d[\d]+$", x),         # noqa: W605
        # ^^^ is a legitimate use of '\d', don't remove the warning.
    )
    try:
        answer = int(inquirer.prompt(int_modify_question)["property"].strip())
        if inquirer.confirm(
            f"Are you sure you want to change {colorama.Fore.BLUE}{property}{colorama.Fore.RESET} to {colorama.Fore.YELLOW}{answer}{colorama.Fore.RESET}"   # noqa: E501
        ):
            return (True, answer)
        return (False, None)
    except ValueError as ve:
        raise ve


def check_is_modified(val, out):
    if val:
        return out
    return ""


# --- CLI SPECIFIC VARIABLES
CLI_VARS_PRETTYPRINT: str = (
    colorama.Fore.BLUE
    + "{}: "
    + colorama.Fore.YELLOW
    + "{}"
    + colorama.Fore.RESET
)
# def get_vars_prettyprint(choice: str):
#     values = choice.split(":")
#     return (values[0].strip(), values[1].strip())
