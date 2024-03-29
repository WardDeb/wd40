import setuptools


setuptools.setup(
   name='wd40',
   version='0.0.1',
   description='Stuff to make my life easier.',
   author="Deboutte",
   author_email="deboutte@ie-freiburg.mpg.de",
   scripts=['bin/wd40'],
   packages=['wdforty'],
   include_package_data=False,
   install_requires=['configparser',
                     'psutil',
                     'Biopython',
                     'matplotlib',
                     'flake8',
                     'rich',
                     'pandas',
                     'numpy',
                     'pytest'],
   python_requires='>3'
)
