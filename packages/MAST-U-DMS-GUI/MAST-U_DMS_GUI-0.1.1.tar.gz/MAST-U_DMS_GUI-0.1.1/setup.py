from setuptools import setup
from setuptools import find_packages


#pull from readme the information
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'MAST-U_DMS_GUI',

    version = '0.1.1',

    #Who to put as the author?
    author = 'Gareth Williams',

    author_email = 'gw878@york.ac.uk',

    description = 'A GUI for spectral data analysis at MAST-U',

    long_description = long_description,

    long_description_content_type = 'text/markdown',

    install_requires=[
        'tkinter==',
        'matplotlib==',
        'pandas==asa',
        'time==',
        'spe2py==',
        'numpy==',
        'scipy==',
    ],

    packages=find_packages(
        include=['MAST-U_DMS_GUI', 'MAST-U_DMS_GUI']

    ),
    include_package_data=True,

    python_requires='>=3.7',


)


