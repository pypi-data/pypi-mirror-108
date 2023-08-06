# Print_dir - it`s a directory-visualizer python-package
## How to install
pip install print_dir
## Guide

```python
from print_dir.visualizer import Visualizer

# You can start work with files from where you would
my_dir = my_dir = Visualizer(directory)  # directory – path to start visualizer

# You can see content of directory
my_dir.dir()

# You can change directory
my_dir.cd(to)  # to – path to new folder

# Via cd-method you can move back
my_dir.cd('..')  # if to == '..' directory changes to parent
```
## Example of usage

```python
from print_dir.visualizer import Visualizer

my_dir = Visualizer('/files/directory/')
my_dir.dir()  # OUTPUT:
"""
📁 directory
|_ 📁 print_dir
|_ 📁 tests
|_ 📁 venv
|_ 📃 .gitignore
|_ 📃 README.md
|_ 📃 setup.py
"""
my_dir.cd('tests')
my_dir.dir()  # OUTPUT:
"""
📁 tests
|_ 📃 test_Visualizer.py
|_ 📃 __init__.py
"""

```