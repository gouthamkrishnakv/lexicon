from enum import Enum
import inquirer


# author type
class AuthorType(Enum):
    STUDENT = "Student"
    FACULTY = "Faculty"
    # GROUP = "Group"


# author
# TODO: Add a group type which holds a list of members
class Author:
    # --- CLASS MEMBERS (INSTANCE VARIABLES) ---
    # type of author
    type: AuthorType
    # author name
    name: str

    # --- CLASS VARIABLES
    NAME = "Name"
    TYPE = "Type"


    # constructor
    def __init__(self, type: AuthorType, name: str) -> None:
        self.type = type
        self.name = name

    def to_dict(self):
        return {
            Author.NAME: self.name,
            Author.TYPE: self.type.name
        }

    # create an author object
    @staticmethod
    def create_author():
        author_query = inquirer.List(
            'author_type',
            'Select the type of author you want',
            list(map(lambda x: str(x)[11:], list(AuthorType)))
        )
        author_name = inquirer.Text(
            'author_name',
            'Enter the name of the {author_type}'
        )
        answer = inquirer.prompt([author_query, author_name])
        try:
            return Author(
                AuthorType(
                    answer['author_type'].capitalize()
                ),
                answer['author_name']
            )
        except TypeError as te:
            print(te)
            raise te
