from setuptools import setup 

with open("README.md", 'r') as f:
    long_description = f.read()

setup( 
    name='handyfuncs', 
    version='0.0.2', 
    description='Handy functions for manipulating data and automating processes',
    author='Porte Verte', 
    author_email='porte_verte@outlook.com', 
    url='https://github.com/porteverte/handyfuncs',
    packages=['handyfuncs'],
    package_dir={'':'src'},
    python_requires=">=3.8",
)