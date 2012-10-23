#!/usr/bin/env python

import sys, os.path
try:
    from minipowerpc.cli import Cli
except:
    sys.path.append(os.path.abspath('../.'))
    from minipowerpc.cli import Cli

if __name__ == '__main__':
    cli = Cli(sys.argv[1:])
    cli.run()

