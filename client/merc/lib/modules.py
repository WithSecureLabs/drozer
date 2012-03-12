#!/usr/bin/python
#
# License: Refer to the README in the root directory
#

import os, os.path, sys
import argparse, shlex
from basecmd import BaseCmd

class Module(object):

    def __init__(self):
        """ Non-existent constructor """
        self.path = "miscellaneous"

    def execute(self, session, arg):
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
Reloads all the modules and regenerates the list of classes 
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
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'list', add_help = False)
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
        except:
            pass

    def do_run(self, args):
        """
Run a custom module
usage: run [--arg <arg>] module
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'run', add_help = False)
        parser.add_argument('module')
        parser.add_argument('--arg', '-a', metavar = '<arg>')

        try:

            # Split arguments using shlex - this means that parameters with spaces can be used - escape " characters inside with \
            splitargs = parser.parse_args(shlex.split(args))

            # Load module
            mod = self.modules.get(splitargs.module, None)

            if (mod):
                # Instantiate the module and execute it
                mod.execute(self.session, splitargs.arg if splitargs.arg else None)
            else:
                print "\nFailed to execute module\n"

        # FIXME: Choose specific exceptions to catch
        except:
            pass

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
        """

        # Define command-line arguments using argparse
        parser = argparse.ArgumentParser(prog = 'info', add_help = False)
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
        except:
            pass

    def complete_info(self, _text, line, _begidx, _endidx):
        
        # Autocompletion on modules
        return [
                mod for mod in sorted(self.modules)
                 if mod.startswith(_text)
            ]

