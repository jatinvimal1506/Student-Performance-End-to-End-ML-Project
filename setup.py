from setuptools import find_packages,setup

#use of setup.py is to consider the current folder as a package and install it when run using -e .
hypen_e_dot = "-e ."
def get_requirements(file_path):
    with open(file_path, "r") as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]

        if hypen_e_dot in requirements:
            requirements.remove(hypen_e_dot)

    return requirements
setup(
    name = "cute-ml-project",
    version = "0.0.1",
    author =  "Jatin",
    author_email= "jatinkvimal@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)

