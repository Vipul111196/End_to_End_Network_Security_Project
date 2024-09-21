'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''

# Importing required libraries
from setuptools import find_packages,setup # Importing setup and find_packages from setuptools
from typing import List 

def get_requirements()->List[str]:
    """
    This function will return list of requirements from requirements.txt file
    """
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r') as file:
            #Read lines from the file
            lines=file.readlines()
            ## Process each line
            for line in lines:
                requirement=line.strip()
                ## ignore empty lines and -e .
                if requirement and requirement!= '-e .': # Ignoring -e . because it is the package itself
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Vipul Tyagi",
    packages=find_packages(),
    install_requires=get_requirements()
)