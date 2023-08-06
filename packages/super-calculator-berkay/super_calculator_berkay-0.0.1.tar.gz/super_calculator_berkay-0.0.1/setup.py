import os
import setuptools
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 2 - Pre-Alpha',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
  'Programming Language :: Python :: 3',
]

with open('README.md') as f:
    long_description = f.read()

# get all data dirs in the datasets module
data_files = []

# Once we have data?
# for item in os.listdir("geopandas/datasets"):
#     if not item.startswith("__"):
#         if os.path.isdir(os.path.join("geopandas/datasets/", item)):
#             data_files.append(os.path.join("datasets", item, "*"))
#         elif item.endswith(".zip"):
#             data_files.append(os.path.join("datasets", item))

#data_files.append("tests/*")
        
setup(
  name='super_calculator_berkay',
  version='0.0.1',
  description='A package to do arithmetics',
  long_description=long_description,
  long_description_content_type='text/markdown',  
  author='berkay',
  author_email='berkayyibis@hotmail.com',
  license='GNU General Public License v2.0', 
  classifiers=classifiers,
  keywords=['math'], 
  package_dir={'':'src'},
  packages=setuptools.find_packages(where="src"),
)
#package_data={"geopandas": data_files},
