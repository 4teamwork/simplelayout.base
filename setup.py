from setuptools import setup, find_packages
import os

version = '3.0c2'

tests_require = [
    'plone.app.testing',
    'plone.mocktestcase',
    ]

setup(name='simplelayout.base',
      version=version,
      description="SimpleLayout is an easy to use plone package for "
      "creating content pages",
      long_description=(open("README.rst").read() + "\n" +
                        open(os.path.join("docs", "HISTORY.txt")).read()),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/simplelayout.base',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['simplelayout'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'archetypes.schemaextender',
        'simplelayout.types.common',
        'simplelayout.ui.base',
        'simplelayout.ui.dragndrop'
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
