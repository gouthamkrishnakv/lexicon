# Lexicon Project Specification

This is a single instance of a project which holds all information relevant to the project in a single file.

This consists of the following

- [`Subprojects`](SUBPROJECTS.md)

    This holds the subprojects of a single project. A project can consist of zero or more subprojects, depending on what the use-case is.

- [`Configuration`](PROJECT.md)

    This holds the configurations of the project used.

- [`Logs`](LOGS.md) (**NOT COMPLETED**)

    This holds the logs of the project, if that is needed for either debugging the project or to check whether there was any malpractice, if needed.

- `Author` or `Authors`

    This holds the information of the author of the project or a list of multiple authors for the project.

### The Project has these variables put in a `lexicon.yaml` file in the root of the project.

---
## Project Directory Tree Specification

**(Configuration specifications reside in the [Project File](PROJECT.md))**

```bash
project\
|- subproject_1\
|  |- file1.v
|  |- file2.v
|  |- file3.v 
|  |- file4.v_
|  |- lexicon_sub.yaml
|  subproject_2\
|  |- file1_mod.v
|  |- file1_tb.v
|  |- lexicon_sub.yaml
|- lexicon.yaml
```
