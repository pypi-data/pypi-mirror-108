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

        |-hellototi.py    **contains a function called say_hello()**
    
        |-__init__.py     ** empty**
