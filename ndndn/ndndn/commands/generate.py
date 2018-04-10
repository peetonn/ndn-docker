"""generate command."""

import sys, os, shutil, re, copy
from json import dumps
from .base import Base


class Generate(Base):
    """Generates Docker-Compose setup for NDN experiment"""

    def run(self):
        print('Hello, generate!')
        print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))

