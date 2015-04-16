#!/usr/bin/env python
#

from distutils.core import setup

setup(name         = 'Topology',
      version      = '2.2.2',
      description  = 'Python bindings for NEST Topology module',
      author       = 'The NEST Initiative',
      url          = 'http://www.nest-initiative.org',     
      packages     = ['nest.topology', 'nest.topology.tests'],
      package_dir  = {'nest.topology': '/Users/atwood/tem/Neu/projects/NEST-SCModel/nest-2.2.2/topology/pynest',
                      'nest.topology.tests': '/Users/atwood/tem/Neu/projects/NEST-SCModel/nest-2.2.2/topology/pynest/tests'})
