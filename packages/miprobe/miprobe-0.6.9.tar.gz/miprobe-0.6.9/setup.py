from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.6.9' 
DESCRIPTION = 'MiProbe Sensor Serial Logging Tool.'
LONG_DESCRIPTION = long_description

setup(
        name="miprobe", 
        version=VERSION,
        author="Evan Taylor",
        author_email="evan@evantaylor.pro",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=['urllib3', 'argparse', 'pyserial', 'pytz', 'tqdm', 'flask', 'simplejson'], # add any additional packages that 
        setup_requires=['wheel'],
        keywords=['miprobe', 'serial', 'sensors', 'biosensor', 'dynamodb', 'logger'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "Operating System :: POSIX :: BSD :: FreeBSD",
            "License :: OSI Approved :: MIT License",
        ],
        url='https://gitlab.com/evantaylor/miprobe',
        scripts=['bin/miprober']
)
