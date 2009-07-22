from setuptools import setup, find_packages
import os

version = '2.0b2'

setup(name='simplelayout.base',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Mathias LEIMGRUBER (4teamwork)',
      author_email='m.leimgruber@4teamwork.ch',
      url='http://psc.4teamwork.ch/oss/simplelayout/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'simplelayout.types.common<=2.1',
          'simplelayout.ui.base<=2.0', 
          'simplelayout.ui.dragndrop<=2.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
