
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- Project: lucidmode                                                                                  -- #
# -- Description: A Lightweight Framework with Transparent and Interpretable Machine Learning Models     -- #
# -- setup.py: python script with setup directives functions                                             -- #
# -- Author: IFFranciscoME - if.francisco.me@gmail.com                                                   -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- Repository: https://github.com/lucidmode/lucidmode                                                  -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

""" A Lucid Framework for Transparent and Interpretable Machine Learning Models. """

# library dependencies to build
import io
import os
import sys
import lucidmode
from shutil import rmtree
from setuptools import find_packages, setup, Command

with open("README.rst", "r") as fh:
    long_description = fh.read()

# Package meta-data.
NAME = 'lucidmode'
DESCRIPTION = 'Interpretable Machine Learning Models'
URL = 'https://github.com/lucidmode/lucidmode'
EMAIL = 'if.francisco.me@gmail.com'
AUTHOR = 'IFFranciscoME'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = lucidmode.__version__

# Packages are required for this module to be executed
REQUIRED = ['pandas', 'numpy', 'rich', 'matplotlib', 'plotly', 'seaborn']

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
try:
    with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """
    Automated upload support process for setup.py
    """

    description = 'Build and publish the package on pypi.org'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload dist/*')

        # -- disable pushing with tags to make quick tests
        # self.status('Pushing git tags ...')
        # os.system('git tag v{0}'.format(about['__version__']))
        # os.system('git push --tags')

        sys.exit()

# Pass arguments for publishing via twine:

setup(name=NAME,
      version=about['__version__'],
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/x-rst',
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,

      python_requires=REQUIRES_PYTHON,
      install_requires=REQUIRED,
      
      packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),

      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.8',
                   'Operating System :: Unix',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS',
                   'Topic :: Scientific/Engineering :: Artificial Intelligence',
                   'Topic :: Scientific/Engineering :: Visualization'],
    
      # $ setup.py publish support.
      cmdclass={'upload': UploadCommand,},
)
