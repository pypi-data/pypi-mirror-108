"""
Setup script
"""
import os
from setuptools import setup, find_packages

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def _post_install():
    print("Installing z3...")
    os.system("pysmt-install --z3 --confirm-agreement")
    os.system("export PYSMT_CYTHON=0")
    # PYSMT_CYTHON = 0


setup(name='paml_check',
      version='0.1',
      description='PAML Checker',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/SD2E/paml-check',
      author='Dan Bryce',
      author_email='dbryce@sift.net',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
          # "paml" This requires that paml have a valid package name
          "pysmt",
          "sbol3"
      ],
      tests_require=["pytest"],
      zip_safe=False
      )

_post_install()
