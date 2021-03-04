# Lexicon Project Specification

### The project consists of 2 parts:

- `Project`

    This is a single instance of a project which holds all information relevant to the project in a single file.

    This consists of the following

    - [`Subprojects`](SUBPROJECTS.md)
    
        This holds the subprojects of a single project. A project can consist of zero or more subprojects, depending on what the use-case is.

    - [`Configuration`](CONFIGURATION.md)

        This holds the configurations of the project used.

    - [`Logs`](LOGS.md)

        This holds the logs of the project, if that is needed for either debugging the project or to check whether there was any malpractice, if needed.

- `Author` or `Authors`

    This holds the information of the author of the project or a list of multiple authors for the project.

### The Project has these variables put in a `lexicon.yaml` file in the root of the project.