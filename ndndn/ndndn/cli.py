"""NDN Docker Net (ndndn)

Usage:
  ndndn generate -t=<dot_file> -a=<app_desc> [-h=<hub_desc> -c=<consumer_env> -p=<producer_env> -o=<out_dir> --copy]
  ndndn run [SETUP_DIR | -s=<setup_dir>]
  ndndn --help
  ndndn --version

Options:
  --help                      Show this screen.
  --version                   Show version.
  -t,--topology=<dot_file>    Exeperiment topology .dot file
  -h,--hub=<hub_desc>         Path to a folder containing hub description [default: ./hub]
  -a,--app=<app_desc>         Path to a folder containing app description
  -c,--cenv=<consumer_env>    Consumer environment file
  -p,--penv=<producer_env>    Producer environment file
  -o,--out=<out_dir>          Output directory [default: ./test1]
  --copy                      Copy descriptions into output directory instead of symlinking them
  -s,--setup=<setup_dir>      Directory that contains generated experiment setup [default: ./]

"""

from inspect import getmembers, isclass
from docopt import docopt
from . import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import ndndn.commands
    options = docopt(__doc__, version=VERSION)

    for (k, v) in options.items(): 
        if hasattr(ndndn.commands, k) and v:
            module = getattr(ndndn.commands, k)
            ndndn.commands = getmembers(module, isclass)
            command = [command[1] for command in ndndn.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
