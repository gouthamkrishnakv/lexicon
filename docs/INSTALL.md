# Installation

`Lexicon` needs **GNU Make** (`make`), **Icarus Verilog** (`iverilog`) and **GTKWave** (`gtkwave`) to run, as the Generated Makefiles require the former to run. We'll install these first.

Then we'll follow up with installing [`Lexicon`](#install-lexicon).

## Tools

**NOTE**: If you're in **MacOS** or **Windows**, Make sure to install [Homebrew](https://brew.sh) (MacOS) or [Chocolatey](https://chocolatey.org) (Windows) before starting.

-   GNU Make (`make`)

	A `Makefile` recipe is output by the Lexicon, after importing settings from the configuration files. [GNU Make](https://www.gnu.org/software/make/) runs this recipe to build modules.

	- Debian-based Systems (Debian, Ubuntu, Pop!_OS, ElementaryOS etc.)

		```bash
		sudo apt update && sudo apt install build-essential -y
		```

	- RPM-based Systems (Fedora, Red Hat Enterprise Linux, CentOS)

		```bash
		sudo dnf groupinstall "C Development Tools and Libraries" -y
		```

        **OR** (for older RPM-based distributions)

        ```bash
        sudo yum install @c-development -y
        ```

    - Arch Linux

        ```bash
        sudo pacman -S --noconfirm base-devel
        ```

	- MacOS (Homebrew)

        ```bash
        brew install make
        ```

    - Windows (Chocolatey)

        ```bash
        choco install make -y
        ```

-   Icarus Verilog (`iverilog`)

    [Icarus Verilog](https://iverilog.icarus.com/) (`iverilog`) is an open-source Verilog Compiler. It compiles a verilog program and executes the program, like it executes any other program.

    - Debian-based Systems (Debian, Ubuntu, Pop!_OS, ElementaryOS etc.)

		```bash
		sudo apt install iverilog -y
		```

	- RPM-based Systems (Fedora, Red Hat Enterprise Linux, CentOS)

		```bash
		sudo dnf install iverilog -y
		```

        **OR**

        ```bash
        sudo yum install iverilog -y
        ```

    - Arch Linux

        ```bash
        sudo pacman -S --noconfirm iverilog
        ```

	- MacOS (Homebrew)

        ```bash
        brew install icarus-verilog
        ```

    - Windows

        Icarus Verilog for Windows is available [here](https://bleyer.org/icarus/). Download and install the latest version (usually the first link).

-   GTKWave (`gtkwave`)

    [GTKWave](https://gtkwave.sourceforge.net/) (`gtkwave`) is an open-source waveform viewer. It's written using the GTK UI and can open `.vcd` files, which is used by Verilog to output variables.

    - Debian-based Systems (Debian, Ubuntu, Pop!_OS, ElementaryOS etc.)

		```bash
		sudo apt install gtkwave -y
		```

	- RPM-based Systems (Fedora, Red Hat Enterprise Linux, CentOS)

		```bash
		sudo dnf install gtkwave -y
		```

        **OR**

        ```bash
        sudo yum install gtkwave -y
        ```

    - Arch Linux

        ```bash
        sudo pacman -S --noconfirm gtkwave
        ```

	- MacOS (Homebrew)

        ```bash
        brew install --cask gtkwave
        ```

    - Windows (Chocolatey)

        ```bash
        choco install gtkwave -y
        ```

## Install Lexicon

1.  Install Python3 `pip` (Python Package Installer)

    - Debian-based Systems (Debian, Ubuntu, Pop!_OS, ElementaryOS etc.)

        ```bash
        sudo apt install python3-pip -y
        ```

    - RPM-based Systems (Fedora, Red Hat Enterprise Linux, CentOS)

        ```bash
        sudo dnf install python3-pip -y
        ```

        **OR**

        ```bash
        sudo yum install python3-pip -y
        ```

    - Arch Linux

        ```bash
        sudo pacman -S --noconfirm python-pip
        ```

    - MacOS (Homebrew)

        ```bash
        brew install python3
        ```

    - Windows (Chocolatey)

        ```bash
        choco install python3 -y
        ```

2.  Install Lexicon

    Open a new Terminal/PowerShell window and **paste**/**type** the following

    ```bash
    pip3 install lexicon-gauthamkrishna9991
    ```
