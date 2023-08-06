#!/usr/bin/env python
import sys
from os.path import exists
from setuptools import setup, Command, find_packages
import versioneer
from shutil import rmtree
import os

here = os.path.abspath(os.path.dirname(__file__))
class UploadCommand(Command):
    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Removing build files...")
        os.system("rm -rf *.egg-info")
        os.system("rm -rf build")
        os.system("rm -rf dist")

        # self.status("Pushing git tags…")
        # os.system("git tag v{0}".format(about["__version__"]))
        # os.system("git push --tags")

        sys.exit()


class InstallCommand(Command):
    description = 'Build and install the package.'
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

        self.status('Building Source and install to local…')
        os.system('{0} setup.py install'.format(sys.executable))

        self.status('Removing build files...')
        os.system('rm -rf *.egg-info')
        os.system('rm -rf build')
        os.system('rm -rf dist')

        sys.exit()

about = {}
VERSION = None
FOLDER = "kitoolz"
if not VERSION:
    with open(os.path.join(here, FOLDER, "__version__.py")) as f:
        exec(f.read(), about)
else:
    about["__version__"] = VERSION

setup(name='kitoolz',
      version=about["__version__"],
      cmdclass={
          # $ python setup.py pypi    # upload repository to pypi
          "pypi": UploadCommand,
          'get': InstallCommand,  # install package to local
      },
      # cmdclass=versioneer.get_cmdclass(),
      description='List processing tools and functional utilities',
      url='https://github.com/szj2ys/kitoolz.git',
      author='https://raw.github.com/pytoolz/toolz/master/AUTHORS.md',
      maintainer='Erik Welch',
      maintainer_email='erik.n.welch@gmail.com',
      license='BSD',
      keywords='functional utility itertools functools',
      packages=['kitoolz',
                'kitoolz.sandbox',
                'kitoolz.curried',
                'tlz'],
      package_data={'kitoolz': ['tests/*.py']},
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      long_description_content_type="text/markdown",
      zip_safe=False,
      python_requires=">=3.5",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "License :: OSI Approved :: BSD License",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy"])
