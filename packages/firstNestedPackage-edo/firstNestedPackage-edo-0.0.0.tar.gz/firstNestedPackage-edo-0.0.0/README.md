# Introduction
A template of a python project with nested packages.


# Project structure:
Python allows flexibity in defining the structure of the project,
Here we show an example:
- ```LICENSE.md```: Your project's license.
- ```README.md```: A description of your project and its goals.
- ```.gitignore```: A file that tells Git what files and directories to ignore. 
- ```example_pkg```: A directory with the name of your project.
- ```requirements.txt```: A file where you can defines outside Python dependencies and their versions for your package.

```
├── docs
├── example_pkg                 Top-level package
│   ├── __about__.py
│   ├── core.py
│   ├── __init__.py
│   ├── sub_pkg_1
│   │   ├── __init__.py
│   │   ├── mod_one.py
│   │   ├── mod_two.py
│   │   └── nested_pkg_1
│   │       ├── __init__.py
│   │       └── nst_1.py
│   ├── sub_pkg_2
│   │   ├── __init__.py
│   │   ├── mod_1.py
│   │   └── mod_2.py
│   └── supporters.py
├── .gitignore                  
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
└── tests


```
## Importing functions:

What is imported in ```__init__.py``` ; can be called using the dot notation when the directory is imported as
package.
for example, in the nested_pkg_1 directory we import ```nested_function()``` from ```nst_1.py```
in ```nested_pkg_1/__init__.py```
```
# nested_pkg_1/__init__.py
# Import functions from the modules in the package nested_pkg_1
from example_pkg.sub_pkg_1.nested_pkg_1.nst_1 import nested_function
```

## Importing modules:

## Importing packages:
Then in sub_pkg_1/__init__.py, Then we import the nested_pkg_1  
```
# Import nested_pkg_1
from example_pkg.sub_pkg_1 import nested_pkg_1
```


When nested_pkg_1 package is imported, nested_function can be called from nested_pgk_1
in example_pkg/core.py
```
# from example_pkg import sub_pkg_1
sub_pkg_1.nested_pkg_1.nested_function()
```

# Testing


# References
- [Python Software Foundation [US]. (2017). Python Packaging User Guide Apr 03, 2020. https://packaging.python.org/](https://packaging.python.org/tutorials/packaging-projects/)
- [The Hitchhicker's Guide to Python](https://docs.python-guide.org/writing/structure/)


# Install
in setup folder run
pip install .

WARNING: using 
```python setup.py install```

the package doesnot show through conda list
Note: Avoid using python setup.py install use ```pip install .```
[https://stackoverflow.com/questions/1550226/python-setup-py-uninstall]

#TODO
try generating wheel and installing the file
```
python3 setup.py sdist bdist_wheel
```
https://packaging.python.org/tutorials/packaging-projects/
