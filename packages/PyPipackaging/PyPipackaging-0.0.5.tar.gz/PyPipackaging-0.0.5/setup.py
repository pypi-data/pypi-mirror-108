from setuptools import setup #setuptools is better than disutil

with open ("README.md", "r") as fh:
    long_description = fh.read()
    
setup(   # lines of configuration
      name='PyPipackaging',             #name is what you PIP install and what you will upload it as. Not the same as py_modules
      version='0.0.5',
      description='Say Hello',
      long_description=long_description,
      long_description_content_type="text/markdown",
      py_modules=["hellototi"],    # list of actual python code modules within src folder
      package_dir={'':'src'},       # says that our code is under a src directory
      url='https://github.com/Totilarson/CorePy',
      author='Toti Larson',
      author_email='totlarson@gmail.com',
      license='LICENSE.txt',
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
      
)

