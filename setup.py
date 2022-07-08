from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.0.1'
DESCRIPTION = 'Gherkin Paperwork'
LONG_DESCRIPTION = ' '


class CustomInstallCommand(install):
    def run(self):
        install.run(self)


# Setting up
setup(
    name="gherkin_paperwork",
    version=VERSION,
    author="Xavier Rodriguez",
    author_email="xavier.rodriguezalvarez@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    cmdclass={'install': CustomInstallCommand},

    # install_requires=[],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
