# Lexicon Module

This is the smallest buildable object in Lexicon. In here, the source files include the test bench and the modules needed for the project. Each module has the following attributes

- `Name` - A unique name for the module for a specific subproject.

- `files` - A list of files which are used for compilation.
    
    **It is recommended that the first file you keep in the list be the test-bench.**

- `files_var` - It is the makefile variable name for the set of file objects for compilation by Icarus Verilog (`iverilog`). This is optional and defaults to `<name in capitals>_FILES`.

- `exec` - The executable file output by `iverilog` and is executed using the command `vvp`. It is optional and defaults to `<name>.vvp`

- `exec_var` - It is the makefile variable for the executable file. This is optional and defaults to `<name in capitals>_EXEC`. Unless you have some name conflicts, this is not needed to be changed.

- `wave` - It is the output file after execution for the wave file. This is usually determined by the user and it is encouraged to write the output file if you put it in the test-bench. Neverthless this is also optional and it defaults to `<name>.vcd`. This opens in GTKWave.

- `wave_var` - This is the makefile variable name for the wave file. This is an optional variable, and unless you have some serious issues building makefiles or have some variable conflicts, you don't really need to use this.

- `build_command` - This is the makefile command for building the executable. It is executed by running `make <build_command>` for the most part. As the module files are already unique keys anyway, and the build commands derive their commands from the module names, there's no real need to change it unless the user needs to. The build commands would be `make <module_name>`.

- `clean_command` - This is the command to clean the workspace of the objects that are inessential for compilaion. This is executed by running `make <clean_command>`. By default the name to clean the workspace is `make <module_name>_clean`.

- `timeout` - This is the amount of time (in seconds) that the executable is allowed to run. It's also optional and it defaults at `10` (command tries to finish before 10s), else exit. If 0 is given, the program would keep on executing incase of a recursive execution.

---

### A SAMPLE MODULE DESCRIPTION


```yaml
and:
  # the file list
  files:
  - and_tb.v
  - and_mod.v
  # exec filename
  exec: and.vvp
  exec_var: AND_EXEC
  # wave file
  wave: and.vcd
  wave_var: AND_WAVE
  # build_command
  build_command: and
  # to clean the workspace
  clean_command: and_clean
  # timeout: 15 seconds
  timeout: 15
```