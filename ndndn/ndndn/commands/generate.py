"""generate command."""

import sys, os, shutil, copy
from distutils.dir_util import copy_tree
from .base import Base

import classes

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
        self.copySetups=False

    def run(self):
        self.generate(self.dotFile)
    
    def generate(self, dotFile):
        # parse nodes from topology
        graphParser = classes.GraphParser()
        self.nodes = graphParser.parseGraph(dotFile)

        # readin env files for producer and consumer
        envReader = classes.EnvReader()
        cenv = envReader.parse(self.consumerEnv) if self.consumerEnv else {}
        penv = envReader.parse(self.producerEnv) if self.producerEnv else {}

        # make yml
        ymlWriter = classes.YmlWriter(self.nodes, cenv, penv)

        if ymlWriter.makeYml():
            # prepare out folder
            outDir = self.createTestFolder()
            self.addDockerDescriptions(outDir)
            graphParser.renderGraph(dotFile, os.path.join(outDir, 'topology.pdf'))
            # write yml
            ymlWriter.writeYml(os.path.join(outDir, 'docker-compose.yml'))
        else:
            print "Failed to create YML configuration for some reason"

    def createTestFolder(self):
        d = self.outDir
        if not self.outDir:
            testNo = 1
            while os.path.exists("./experiment"+str(testNo)):
                testNo += 1
            d = "./experiment"+str(testNo)
            os.makedirs(d)
        elif not os.path.exists(self.outDir):
            os.makedirs(self.outDir)
            d = self.outDir
        return d
    
    def addDockerDescriptions(self, outDir):
        dirs = [os.path.join(outDir, 'h'),
                os.path.join(outDir, 'p'),
                os.path.join(outDir, 'c')]
        for d in dirs:
            if os.path.exists(d) or os.path.islink(d):
                os.remove(d)
        if not self.copySetups:
            os.symlink(os.path.join('..', self.hubDir), os.path.join(outDir, 'h'))
            os.symlink(os.path.join('..', self.appDir), os.path.join(outDir, 'p'))
            os.symlink(os.path.join('..', self.appDir), os.path.join(outDir, 'c'))
        else:
            copy_tree(self.hubDir, dirs[0])
            copy_tree(self.hubDir, dirs[1])
            copy_tree(self.hubDir, dirs[2])



 
