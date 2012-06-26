#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import os.path, sys
import shlex
from basecmd import BaseCmd
from basecmd import BaseArgumentParser

class Module(object):

    def __init__(self):
        """ Non-existent constructor """
        self.path = "miscellaneous"

    def execute(self, session, args):
        """ Abstract execution function """

class Modules(BaseCmd):

    def __init__(self, session):
        BaseCmd.__init__(self, session)
        self.prompt = "*mercury#modules> "
        self.modules = {} # A dictionary of module classes
        self.do_reload(None)

    def _get_subclasses(self, cls):
        """
A recursive function to return all subclasses of a particular class
        """
        for i in cls.__subclasses__():
            for c in self._get_subclasses(i):
                yield c
        yield cls

    def _locate_modules(self):
        """
Locates all the module files under the modules directory
        """
        modnames = {} # A dictionary of modules located
        path = os.path.join(os.path.dirname(__file__), "..", "modules") # Path for the modules directory

        if os.path.exists(path) and os.path.isdir(path):
            for dirpath, _dirnames, filenames in os.walk(path):
                for filename in filenames:

                    # Run through files as we always used to
                    relfile = os.path.join(dirpath[len(path) + len(os.path.sep):], filename)
                    module_path, ext = os.path.splitext(relfile)
                    namespace = ".".join(['merc', 'modules'] + [ x for x in module_path.split(os.path.sep) if x ])

                    # Lose the extension for the module name (here we accept pre-compiled python as well as py files)
                    if ext in [".py", ".pyc", ".pyo"]:
                        filepath = os.path.join(path, relfile)
                        # Handle Init files
                        initstr = '.__init__'
                        if namespace.endswith(initstr):
                            modnames[namespace[:-len(initstr)]] = filepath
                        else:
                            modnames[namespace] = filepath
        return modnames

    def _import_modules(self, modnames):
        """
Imports all the modules listed in modnames
        """
        for i in modnames.keys():
            if modnames[i] is not None:
                try:
                    __import__(i)
                    # Reload the module in case the source has changed
                    # We don't need to be careful over i, because the 
                    # import must have been successful to get here
                    reload(sys.modules[i])
                except BaseException, e:
                    print "Failed to import module", i, " - ", str(e)

    def do_back(self, _args):
        """
Return to main menu
        """
        return -1

    def do_reload(self, _args):
        """
Reloads all the modules and regenerates the list of classes.

Developer note: When developing a new module or changing code, remember to reload before running it in order to make the code changes take effect
        """

        # Build up the list of modules
        modnames = self._locate_modules()
        self._import_modules(modnames)

        # Regenerate the class list
        self.modules = {}
        for cls in self._get_subclasses(Module):
            if cls != Module:
                mod = cls()
                self.modules[".".join(mod.path + [mod.__class__.__name__.lower()])] = mod

    def do_list(self, args):
        """
List all available modules with optional filter
usage: list [--filter <filter>]

Note: it is possible to use -f instead of --filter as shorthand
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'list', add_help = False)
        parser.add_argument('--filter', '-f', metavar = '<filter>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Iterate and display according to filter
            print ""
            for module in sorted(self.modules):
                if (splitargs.filter):
                    if splitargs.filter in module:
                        print module
                else:
                    print module
            print ""

        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def do_run(self, args):
        """
Run a custom module
usage: run module [--args arg=value [arg=value ...]]

These modules are developed by various members of the community, please feel free to contribute new modules! To find out more information about a module, use "info module" 
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'run', add_help = False)
        parser.add_argument('module')
        parser.add_argument('--args', '-a', nargs = '+', metavar = 'arg=value')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Compile stated arguments to send to execute
            args = vars(splitargs)['args']

            # Convert to a dict
            args_dict = {}

            if args:
                for arg in args:
                    split = arg.split('=')
                    if split:
                        args_dict[split[0]] = split[1]

            # Load module
            mod = self.modules.get(splitargs.module, None)

            if (mod):
                # Instantiate the module and execute it
                mod.execute(self.session, args_dict)
            else:
                print "\nFailed to execute module\n"

        # FIXME: Choose specific exceptions to catch
        except Exception, e:
            print "Exception:", str(e)

    def complete_run(self, _text, line, _begidx, _endidx):

        # Autocompletion on modules
        return [
                mod for mod in sorted(self.modules)
                 if mod.startswith(_text)
            ]


    def do_info(self, args):
        """
Get information about a custom module
usage: info module

Type "list" to get a list of all available modules 
        """

        # Define command-line arguments using argparse
        parser = BaseArgumentParser(prog = 'info', add_help = False)
        parser.add_argument('module')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Load module
            mod = self.modules.get(splitargs.module, None)

            if (mod):
                # Instantiate the module and ask for information
                print "\n" + mod.__class__.__doc__ + "\n"
            else:
                print "\nFailed to get info about module\n"


        # FIXME: Choose specific exceptions to catch
        except Exception:
            pass

    def complete_info(self, _text, line, _begidx, _endidx):

        # Autocompletion on modules
        return [
                mod for mod in sorted(self.modules)
                 if mod.startswith(_text)
            ]

