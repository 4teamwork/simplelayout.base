from setuptools import setup, find_packages
import os

version = open('simplelayout/base/version.txt').read().strip()
maintainer = 'Mathias Leimgruber'

setup(name='simplelayout.base',
      version=version,
      description="SimpleLayout is an easy to use plone package for creating content pages",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='%s, 4teamwork GmbH' % maintainer,
      author_email='info@4teamwork.ch',
      maintainer=maintainer,
      url='http://plone.org/products/simplelayout.base/',
      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.schemaextender',
          'simplelayout.types.common<=3.0',
          'simplelayout.ui.base<=2.1',
          'simplelayout.ui.dragndrop<=2.1'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
