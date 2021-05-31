# Lexicon - Projects

- `Name` - This holds the name of the project, something like `Assignment_4`, `Examination_1` or any other user-preferred name, unless the project is necessary to have a specific name, **as long as it only uses letters, numbers and underscores**.

- `Type` - This determines the type of project that the YAML file holds. These are of **4** types:
    - `assignment` - This determines that the type of project is an assignment.
    - `examination` - This determines that the type of project is an examination.
    - `project` - This determines that the type of project is a minor-project.
    - `faculty copy` - This determines that the type of project is a faculty copy.
    - `answer key` - This determines that the type of project is an answer-key.
    - `other` - Any other type of project.

- [`Subprojects`](SUBPROJECTS.md) - This holds the list of subprojects that are in this project. Each subproject is kept in a directory with the same name as given in `Subprojects` list here. Each subproject name is decided by the user, unless the subproject is necessary to have a specific name.

- [`Author`] - Describes the Author of the Project.

---

### A SAMPLE PROJECT DESCRIPTION

#### `lexicon.yaml`

```yaml
Name: Project
Type: project
Author:
  Name: Ramesh Acharya
  Type: student
Subprojects:
- subproject_01
- subproject_02
```