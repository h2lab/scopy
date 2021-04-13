import scopy
from scopy._ifaces import *
from scopy.scopes import *

import sys
import argparse
import matplotlib.pyplot as plt
import code


logo = r"""
  ██████  ▄████▄   ▒█████   ██▓███ ▓██   ██▓
▒██    ▒ ▒██▀ ▀█  ▒██▒  ██▒▓██░  ██▒▒██  ██▒
░ ▓██▄   ▒▓█    ▄ ▒██░  ██▒▓██░ ██▓▒ ▒██ ██░
  ▒   ██▒▒▓▓▄ ▄██▒▒██   ██░▒██▄█▓▒ ▒ ░ ▐██▓░
▒██████▒▒▒ ▓███▀ ░░ ████▓▒░▒██▒ ░  ░ ░ ██▒▓░
▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░░ ▒░▒░▒░ ▒▓▒░ ░  ░  ██▒▒▒
░ ░▒  ░ ░  ░  ▒     ░ ▒ ▒░ ░▒ ░     ▓██ ░▒░
░  ░  ░  ░        ░ ░ ░ ▒  ░░       ▒ ▒ ░░
      ░  ░ ░          ░ ░           ░ ░
         ░                          ░ ░
"""

def main(args):
    """
        scopy Shell
    """
    if not args.scope:
        exit(-1)

    scope = globals()[args.scope](vars(args))

    code.interact(
        local=locals(),
        banner="""

The connection with your scope is opened.

You have access to your scope through the `scope` variable.
        
Type help(scope) for commands lits and descriptions

Type exit() or CTRL-D to exit.

        """,
    )

    sys.exit(0)

def script():
    print(logo) 
    parser = argparse.ArgumentParser(description="Scope controller")

    parser.add_argument(
        "--timeout", type=int, default=47, help="Capture Timeout"
    )
       
    parser.add_argument(
        "--scope", type=str, help="Avaiable scopes: {}".format(", ".join(scopy.__all__))
    )

    for i in scopy._ifaces.__all__:
        iface = globals()[i]
        parser.add_argument("--{}".format(i), action='store_true')
        for p in iface.params:
            parser.add_argument(p[0], type=p[1], help=p[2])
                
    try:
        args = parser.parse_args()
        if args.scope == None:
            raise AttributeError
        main(args)
    except (KeyError, AttributeError) as e:
        parser.print_help()
        sys.exit(-1)

    sys.exit(0)
       

if __name__ == "__main__":
    script()
