
import setuptools

with open("docs/README.md", "r", encoding="utf-8") as readmefile:
    long_description = readmefile.read()

# Set up all things
setuptools.setup(
    name = "lexicon-gauthamkrishna9991",
    version = "0.1.0",
    author = "Goutham Krishna K V",
    author_email = "gauthamkrishna9991@live.com",
    description = "A Verilog Project Management Tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/gauthamkrishna9991/lexicon",
    project_urls = {
        "Issues": "https://github.com/gauthamkrishna9991/issues"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    package_dir = {
        "": "src"
    },
    install_requires = [
        "blessed==1.17.6",
        "colorama==0.4.4",
        "inquirer==2.7.0",
        "python-editor==1.0.4",
        "PyYAML==5.4.1",
        "readchar==2.0.1",
        "six==1.15.0",
        "wcwidth==0.2.5",
    ],
    entry_points = {
        "console_scripts": [
            "lexicon=lexicon.main:main"
        ]
    },
    packages = setuptools.find_packages(where="src"),
    python_requires = ">= 3.6"
)