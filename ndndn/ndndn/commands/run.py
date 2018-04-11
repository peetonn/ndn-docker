"""run command."""

import subprocess, os
from .base import Base

class Run(Base):
    """Runs Docker-Compose setup"""

    def __init__(self, options, *args, **kwargs):
        Base.__init__(self, options, args, kwargs)
        self.setupDir=self.options['SETUP_DIR'] if self.options['SETUP_DIR'] else self.options['--setup']

    def run(self):
        os.chdir(self.setupDir)
        subprocess.call(["docker-compose", "up", "--build", "-d"])
