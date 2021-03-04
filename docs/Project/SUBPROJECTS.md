# Lexicon Subprojects

- `Name` - Name of the subproject.

- `Parent` - Name of the parent, which this subproject is a parent to.

- `Author` -  In case of any project other than for the minor project, the `Author` key is also added to here.

- [`Modules`](MODULE.md) - Each module which correspond to differing builds of a subset of all the files in the project. This is more suited for unit-testing of subprojects and the subsequent writing of projects.

    Each module is a key-value pair, whose key is the name of the module, and value is an object that describe the module. More information can be found [here](MODULE.md).

---
### A SAMPLE SUBPROJECT DESCRIPTION

#### lexicon_sub.yaml

```yaml
Name: Assignment_01_Q01
Parent: Assignment_01
Author: Ramesh Acharya <ramesh_b21xxxxcs@nitc.ac.in> <B21XXXXCS>
Modules:
  not:
    - not_tb.v
    - not_mod.v
  and:
    files:
    - and_tb.v
    - and_mod.v
  or:
    files:
    - or_tb.v
    - or_mod.v
```
