from setuptools import setup
from setuptools import find_packages


#pull from readme the information
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'MAST-U-DMS-GUI',

    version = '0.1.14',

    #Who to put as the author?
    author = 'Gareth Williams',

    author_email = 'gw878@york.ac.uk',

    description = 'A GUI for spectral data analysis at MAST-U',

    long_description = long_description,

    long_description_content_type = 'text/markdown',

    install_requires=[
		'Click',
        'matplotlib>=3.3.4',
        'pandas>=1.2.3',
        'spe2py>=2.0.0',
        'numpy>=1.20.1',
        'scipy>=1.6.1',
    ],
    
	entry_points={
        'console_scripts': [
            'Run_MAST-U_DMS_GUI = MASTUDMSGUI.Updated_for_real_data_GUI_plotter:run_program',
            'Run_MAST-U_DMS_saved_data_plotter = MASTUDMSGUI.GUI_exportated_flies_extractor: main',
        ],
    },
    
    packages=find_packages(
        include=['MASTUDMSGUI', 'MASTUDMSGUI']

    ),
    include_package_data=True,

    python_requires='>=3.7',


)


