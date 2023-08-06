# Packaging Tutorial

This is a tutorial on setting up python packages for PyPi. 
**Steps were learned from:** [Publishing (Perfect) Python Packages on PyPi](https://www.youtube.com/watch?v=GIF3LaRqgXo&t=1281s)

# Notes

1)	From the folder level with setup.py : **python setup.py sdist bdist_wheel**
- Builds a wheel that is appropriate to upload to PyPi
- The name used in the setup.py file is added. This was a point of confusion for me. **this name is what you pip install not necessarily the name of the pythjon code that will be imported**
2)	From the folder level with setup.py : **pip install –e .**
- **installs it locally**. Tests packaging and makes it useful to your system.
- The ‘–e’ allows it to link to the code you are working on rather than building copies . The ‘ .’ means install in the current directory. Everytime you change the setup.py file you need to run this
- The name used in the setup.py file is added. This was a point of confusion for me
3)	Test it:
- from python environment in any folder **from hellototi import say_hello**
- **‘hellototi’** is the python module
- The name **‘PyPipackaging’** is from setup.py -> name=’hellototiname’. It is the name of the python script in the src folder. Within this script is the function say_hello
4)	Remove excessive files with gitignore.io
5)	Pip install twine
- Twine upload dist/*    **user name and pasword from PyPi.com**

# Folder structure
packaging_tutorial

    |-LICENSE.txt         **MIT**

    |-README.md           **edited in markdown**

    |-setup.py            **name=PyPipackaging, package=src, python module=hellototi**

    |-src

        |-pypipackaging.py    **contains functions**
    
        |-__init__.py     ** empty**
        
# Application
1) this package can be installed using **pip install PyPipackaging**
2) once installed the python code can be implemented by typing **from pypipackaging import Funsum** in Python environment
3) In Python interpreter like Spider you can type **import pypipackaging** followed by pypipackaging.Funsum(10,10))
4) I had to restart the kernal in Spyder to recognize the python module



# Notes
1) Install wheel **pip install wheel**
2) **python setup.py sdist bdist_wheel** - this makes sdist build, and .egg-info files in directory
3) **pip install -e .** - this installs it locally so it can be tested. use **pip list** to see local vs. global modules
4) at this point you can use: **import pypipackaging** and **pypipackaging.Funsum(10,10)** from the Python environment. It is locally installed (see pip list from cmd)