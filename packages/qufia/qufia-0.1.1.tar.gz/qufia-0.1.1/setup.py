import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
  name = 'qufia',
  packages = ['qufia'],
  version = '0.1.1',
  license='GNU GPLv3',
  description = 'Fast and extensible access to forest inventory data',
  long_description = README,
  long_description_content_type="text/markdown",
  author = 'Lucas Wells',
  author_email = 'lucas@holtzforestry.com',
  keywords = ['forest inventory and analysis', 'FIA'],
  install_requires=[
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
