import os
import glob
from setuptools import setup, find_packages

from gambitcore.__version__ import __version__ as version

def read(fname):
    """
    Reads a file.
    Args:
        fname (str): The name of the file to read.
    Returns:
        str: The contents of the file.
    Examples:
        >>> read('README.md')
        'This is the contents of the README.md file.'
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='gambitcore',
    version=version,
    description='gambitcore: Calculate core genome completeness against a species',
    long_description=read('README.md'),
    packages = find_packages(),
    author='Andrew J. Page',
    author_email='andrew.page@theiagen.com',
    url='https://github.com/gambit-suite/gambitcore',
    scripts=glob.glob('scripts/*'),
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[
        'biopython >= 1.68',
        'pandas',
        'numpy',
    ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)