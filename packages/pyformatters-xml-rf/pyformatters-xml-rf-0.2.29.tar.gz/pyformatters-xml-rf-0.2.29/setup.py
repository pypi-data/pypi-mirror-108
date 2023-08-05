#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pyformatters_xml_rf']

package_data = \
{'': ['*']}

install_requires = \
['pymultirole_plugins', 'lxml', 'ranger', 'pytest']

entry_points = \
{'pyformatters.plugins': ['xml_rf = pyformatters_xml_rf.xml_rf:RFXmlFormatter']}

setup(name='pyformatters-xml-rf',
      version='0.2.29',
      description='Sherpa XML RF formatter',
      author='Olivier Terrier',
      author_email='olivier.terrier@kairntech.com',
      url='https://kairntech.com/',
      packages=packages,
      package_data=package_data,
      install_requires=install_requires,
      entry_points=entry_points,
      python_requires='>=3.8',
     )
