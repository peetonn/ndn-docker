"""generate command."""

import sys, os, shutil, copy
import yaml
import classes

from json import dumps
from .base import Base


class Generate(Base):
    """Generates Docker-Compose setup for NDN experiment"""

    def __init__(self, options, *args, **kwargs):
        Base.__init__(self, options, args, kwargs)
        self.dotFile=self.options['--topology']
        self.hubDir=self.options['--hub']
        self.appDir=self.options['--app']
        self.consumerEnv=self.options['--cenv']
        self.producerEnv=self.options['--penv']
        self.outDir=self.options['--out']

    def run(self):
        self.generate(self.dotFile)
    
    def generate(self, dotFile):
        # parse nodes from topology
        graphParser = classes.GraphParser()
        self.nodes = graphParser.parseGraph(dotFile)

        print "Here are the nodes so far: "
        for k, node in self.nodes.iteritems():
            print k, ": ", node

 
