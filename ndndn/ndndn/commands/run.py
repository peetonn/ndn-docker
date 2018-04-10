"""run command."""


from json import dumps
from .base import Base

class Run(Base):
    """Runs Docker-Compose setup"""

    def run(self):
        print('Hello, run!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
