from docopt import docopt

from minipowerpc import MiniPC

class Cli(object):
    """Mini PowerPC

Usage:
    minipowerpc-cli.py compile [-d|--debug] <file> [--out=<out>]
    minipowerpc-cli.py run [-d|--debug] <file>
    """

    def __init__(self, argv):
        self.arguments = docopt(self.__doc__, argv=argv, help=True, version=None)
        print self.arguments
        self.pc = MiniPC()
        if self.arguments['-d']:
            self.pc.setDebug()


    def run(self):
        if self.arguments['compile']:
            if self.arguments['--out']:
                out = self.pc.compiler.compile(self.arguments['<file>'], self.arguments['--out'])
            else:
                out = self.pc.compiler.compile(self.arguments['<file>'])
            print "file {} comiled to file {}".format(self.arguments['<file>'], out)
        elif self.arguments['run']:
           self.pc.cpu.mem.load(self.arguments['<file>'])
           self.pc.cpu.run()
           print self.pc.cpu



