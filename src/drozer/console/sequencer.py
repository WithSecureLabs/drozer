import argparse
import re

class Sequencer(object):
    """
    The Sequencer can accept a file as input, and reads commands from the file
    a line at a time, executing them in the provided session.
    """

    def __init__(self, args):
        parser = argparse.ArgumentParser(add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("file", help="file", nargs="?",
            type=argparse.FileType('r'))
        parser.add_argument("args", help="command-line arguments", nargs="*")

        parser.error = self.__parse_error
        
        arguments = parser.parse_args(args)

        self.__sequence = arguments.file.read()
        self.__arguments = arguments.args

    def run(self, session):
        """
        Run the commands, extracted from the source file.
        """

        for command in self.__commands():
            command = self.__do_substitutions(command)
            command = session.precmd(command)
            stop = session.onecmd(command)
            stop = session.postcmd(stop, command)

    def __commands(self):
        """
        Split the source file into a series of commands.

        Currently, we support one command per line.
        """

        return filter(lambda c: c.strip() != "", self.__sequence.split("\n"))

    def __do_substitutions(self, command):
        """
        Performs command-line argument subsitution on a command.
        """

        command = re.subn(r'\$([0-9]+)', self.__do_numbered_subs, command)[0]
        command = re.subn(r'\$([@\^\$])', self.__do_symbol_subs, command)[0]
        
        return command

    def __do_numbered_subs(self, match_object):
        """
        Processes a numbered substitution, retrieving the appropriate argument
        from the command-line options.
        """

        return self.__arguments[int(match_object.group(1))-1]

    def __do_symbol_subs(self, match_object):
        """
        Processes a symbole substitution, retrieving the appropriate argument
        from the command-line options.
        """

        if match_object.group(1) == "@":
            return " ".join(self.__arguments)
        if match_object.group(1) == "^":
            return self.__arguments[0]
        if match_object.group(1) == "$":
            return self.__arguments[-1]
        
    def __parse_error(self, message):
        """
        Exception handler, to override the default ArgumentParser logic, which
        is to show usage information and quit.
        """

        raise Exception(message)
