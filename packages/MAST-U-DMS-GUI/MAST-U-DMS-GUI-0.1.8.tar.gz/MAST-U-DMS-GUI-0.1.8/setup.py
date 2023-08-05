from setuptools import setup
from setuptools import find_packages


#pull from readme the information
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'MAST-U-DMS-GUI',

    version = '0.1.8',

    #Who to put as the author?
    author = 'Gareth Williams',

    author_email = 'gw878@york.ac.uk',

    description = 'A GUI for spectral data analysis at MAST-U',

    long_description = long_description,

    long_description_content_type = 'text/markdown',

    install_requires=[
        'matplotlib>=3.3.4',
        'pandas>=1.2.3',
        'spe2py>=2.0.0',
        'numpy>=1.20.1',
        'scipy>=1.6.1',
    ],

    packages=find_packages(
        include=['MASTUDMSGUI', 'MASTUDMSGUI']

    ),
    include_package_data=True,

    python_requires='>=3.7',


)


