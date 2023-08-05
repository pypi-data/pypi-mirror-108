from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
      name='groupBMC',
      version='1.0',
      author='Sichao Yang',
      author_email='sichao@cs.wisc.edu',
      description='Bayesian Model Comparison for Group Studies',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/cpilab/group-bayesian-model-comparison.git',
      packages=find_packages(),
      )
