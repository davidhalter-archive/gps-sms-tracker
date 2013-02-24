#!/usr/bin/env python
"""
GPS/SMS tracking with Fusion Tables

Usage:
  run.py
  run.py add <name> <number>

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
from docopt import docopt

import config

arguments = docopt(__doc__, version='0.1')

if arguments['<name>'] is not None:
    config.add_contact(arguments['<name>'], arguments['<number>'])
else:
    print config.get_token()
