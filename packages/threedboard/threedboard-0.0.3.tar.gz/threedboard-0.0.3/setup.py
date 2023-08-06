from setuptools import setup, find_packages
import distutils.cmd
import os
import distutils.log
import setuptools
import setuptools.command.build_py
import subprocess
from os import path
from subprocess import check_output

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

class BuildDashboardCommand(distutils.cmd.Command):

  description = 'build the 3db dashboard'
  user_options = [
      # The format is (long option, short option, description).
  ]

  def initialize_options(self):
    """Set default values for options."""
    # Each user option must be listed here with their default value.

  def finalize_options(self):
    """Post-process options."""
    pass


  def run(self):
    """Run command."""
    command = ['/bin/bash', path.join(os.getcwd(), 'build_dashboard.sh')]
    self.announce(
        'Running command: %s' % str(command),
        level=distutils.log.INFO)
    r = subprocess.check_output(command)


setup(name='threedboard',
      version='0.0.3',
      description='Web Interface to visualize the results of 3DB experiments',
      url='https://github.com/3db/dashboard',
      author='3DB authors',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='leclerc@mit.edu',
      license='MIT',
      install_requires=[
        'webbrowser',
        'flask',
        'flask_cors',
        'numpy',
        'tqdm',
        'flask-compress'],
      packages=find_packages(),
      cmdclass={
          'build_dashboard': BuildDashboardCommand
      },
      include_package_data=True,
      zip_safe=False)
