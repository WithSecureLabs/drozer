import itertools
import re
import shlex
import socket
import sys
import textwrap
import traceback

from mwr.common import cmd_ext as cmd
from mwr.common import console
from mwr.common.list import flatten
from mwr.common.text import wrap

from mwr.droidhg.api.protobuf_pb2 import Message
from mwr.droidhg.console.coloured_stream import ColouredStream
from mwr.droidhg.console.sequencer import Sequencer
from mwr.droidhg.modules import common, Module
from mwr.droidhg.reflection import Reflector
from mwr.droidhg.repoman import ModuleManager

class Session(cmd.Cmd):
    """
    Mercury: the Heavy Metal that Poisoned the Droid

    Type `help COMMAND` for more information on a particular command, or `help MODULE` for a particular module.
    """

    def __init__(self, server, session_id):
        cmd.Cmd.__init__(self)

        self.__base = ""
        self.__reflector = Reflector(self)
        self.__server = server
        self.__session_id = session_id

        self.active = True
        self.aliases = { "ls": "list" }
        self.intro = "Mercury Console"
        self.history_file = ".mercury_history"
        self.prompt = "mercury> "
        self.stdout = ColouredStream(self.stdout)
        self.stderr = ColouredStream(self.stderr)

    def completefilename(self, text, line, begidx, endidx):
        """
        Provides readline auto-completion for filenames on the local (Console)
        file system.
        """

        return common.path_completion.on_console(text)

    def completemodules(self, text):
        """
        Provides readline auto-completion for Mercury module names.
        """

        if self.__base == "":
            return filter(lambda m: m.startswith(text), self.__modules())
        elif text.startswith("."):
            return filter(lambda m: m.startswith(text[1:]), self.__modules())
        else:
            return map(lambda m: m[len(self.__base):], filter(lambda m: m.startswith(self.__base + text), self.__modules()))

    def completenamespaces(self, text):
        """
        Provides readline auto-completion for Mercury namespaces.
        """

        if self.__base == "":
            return filter(lambda m: m.startswith(text), self.__namespaces())
        elif text.startswith("."):
            namespaces = self.__namespaces(global_scope=True)
            namespaces.add("..")

            return map(lambda m: "." + m, filter(lambda m: m.startswith(text[1:]), namespaces))
        else:
            return map(lambda m: m[len(self.__base):], filter(lambda m: m.startswith(self.__base + text), self.__namespaces()))

    def do_cd(self, args):
        """
        usage: cd NAMESPACE

        The namespace is taken as relative to the current location in the module tree:

            mercury> cd information
            mercury#information> cd native
            mercury#information.native>

        To specify an absolute path, prefix it with a period character:

            mercury#information.native> cd .package
            mercury#package>

        It is still possible to run commands from other namespaces, by specifying the absolute path (prefixed by a period) to the `run` command:

            mercury> cd package
            mercury#package> run .activity.info

        Passing an empty string to `cd` will switch back to the root namespace:

            mercury#information.native> cd
            mercury>

        Passing '..' will move up one level:

            mercury#information.native> cd ..
            mercury#information>
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("cd")
            return

        if len(argv) == 0:
            argv.append("")

        if not self.__setBase(argv[0]):
            self.stderr.write("invalid path: %s\n"%argv[0])

    def complete_cd(self, *args):
        """
        Provides readline auto-completion for the `cd` command, suggesting
        namespaces.
        """

        return self.completenamespaces(args[0])

    def do_contributors(self, args):
        """
        Display a list of Mercury contributors.
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("contributors")
            return

        contributors = map(lambda m: Module.get(m).author, Module.all())
        contribution = [(c[0], len(list(c[1]))) for c in itertools.groupby(sorted(flatten(contributors)))]

        self.stdout.write("Core Contributors:\n")
        for contributor in ['MWR InfoSecurity (@mwrlabs)', 'Luander (luander.r@samsung.com)', 'Rodrigo Chiossi (r.chiossi@samsung.com)']:
            self.stdout.write("  %s\n"%contributor)

        self.stdout.write("\nModule Contributors:\n")
        for contributor in sorted(contribution, key=lambda c: -c[1]):
            self.stdout.write("  %s\n"%contributor[0])

    def do_exit(self, args):
        """
        Terminate your Mercury session.
        """
        
        if self.active:
            self.__server.stopSession(self.__session_id)
            
            self.active = False

        return True

    def do_help(self, args):
        """
        usage: help [COMMAND OR MODULE]

        Displays help information.
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("help")
            return

        if len(argv) > 0:
            if self.__module_name(argv[0]) in Module.all() or self.__module_name("." + argv[0]) in Module.all():
                self.do_run(" ".join([argv[0], "--help"]))
            else:
                try:
                    func = getattr(self, 'help_' + argv[0])
                except AttributeError:
                    try:
                        doc = getattr(self, 'do_' + argv[0]).__doc__
                        if doc:
                            self.stdout.write("%s\n" % wrap(textwrap.dedent(str(doc)).strip(), width=console.get_size()[0]))
                            return
                    except AttributeError:
                        pass
                    self.stdout.write("%s\n" % str(self.nohelp) % (argv[0],))
                    return
                func()
        else:
            cmd.Cmd.do_help(self, args)

    def complete_help(self, *args):
        """
        Provides readline auto-completion for the `help` command, offering
        commands, modules and topics.
        """

        commands = set(self.completenames(args[0]))
        modules = set(self.completemodules(args[0]))
        topics = set(a[5:] for a in self.get_names() if a.startswith('help_' + args[0]))

        return list(commands | modules | topics)

    def do_list(self, args):
        """
        usage: list [FILTER]

        Displays a list of the available modules, optionally filtered by name.

        Examples:

            mercury> list
            activity.forintent
            activity.info
            ... snip ...
            mercury> list debug
            information.debuggable
            mercury>
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("list")
            return

        term = len(argv) > 0 and argv[0] or None

        print console.format_dict(dict(map(lambda m: [m, Module.get(m).name], filter(lambda m: term == None or m.find(term.lower()) >= 0, self.__modules()))))

    def do_load(self, args):
        """
        usage: load FILE

        Loads a file, and executes it as a script.
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("load")
            return

        if len(argv) > 0:
            try:
                Sequencer(argv).run(self)
            except KeyboardInterrupt:
                self.stderr.write("\nCaught SIGINT. Interrupt again to terminate you session.\n")
            except Exception as e:
                self.handleException(e)
        else:
            self.do_help("load")

    def complete_load(self, text, line, begidx, endidx):
        """
        Provides readline auto-completion for the `load` command, offering
        local file names.
        """

        return self.completefilename(text, line, begidx, endidx)

    def do_module(self, args):
        """
        module [COMMAND] (inside Mercury)
    
        Run the Mercury Module and Repository Manager.
    
        The Repository Manager handles Mercury modules and module repositories.
        """
        
        ModuleManager().run(shlex.split(args, comments=True))
        Module.reload()
        
    def do_run(self, args):
        """
        usage: run MODULE [OPTIONS]

        To see the options for a particular module, run `help MODULE`.
        """
        argv = shlex.split(args, comments=True)

        if len(argv) == 1 and (argv[0] == "-h" or argv[0] == "--help"):
            self.do_help("run")
            return

        if len(argv) > 0:
            try:
                module = self.__module(argv[0])
            except KeyError as e:
                self.stderr.write("unknown module: %s\n" % str(e))
                return None

            try:
                module.run(argv[1:])
            except KeyboardInterrupt:
                self.stderr.write("\nCaught SIGINT. Interrupt again to terminate you session.\n")
            except Exception as e:
                self.handleException(e)
        else:
            self.do_help("run")

    def complete_run(self, text, line, begidx, endidx):
        """
        Provides readline auto-completion for the `run` command.

        If auto-completion is requested on the first token after the 'run'
        command, we offer module names. Otherwise, we delegate to the complete()
        method defined on the specified module.
        """

        _line = re.match("(run\s+)([^\s]*)(\s*)", line)

        # figure out where the module name starts in the string
        cmdidx = len(_line.group(1))

        if begidx == cmdidx:
            # if we are trying to autocomplete the module name, offer modules as suggestions
            return self.completemodules(text)
        else:
            # otherwise, we are trying to autocomplete some options for the module, and should
            # defer to it
            offset = len(_line.group(0))
            # we pass over the arguments for autocompletion, but strip off the command and module
            # name for simplicity
            return self.__module(_line.group(2)).complete(text, line[offset:], begidx - offset, endidx - offset)

    def do_shell(self, args):
        """
        usage: `! [COMMAND]` or `shell [COMMAND]`

        Execute a Linux command in the context of Mercury.

        If a COMMAND is specified, this is shorthand for `run shell.exec COMMAND`. Otherwise, it will launch an interactive shell.

        Example:

            mercury> ! date
            Fri Dec 21 23:59:59 GMT 2012
            mercury> ! cat /etc/hosts
            127.0.0.1  localhost

        The working directory of your shell will be the Mercury Agent root folder.
        """

        if len(args) > 0:
            return self.do_run(".shell.exec \"%s\"" % args)
        else:
            return self.do_run(".shell.start")

    def sendAndReceive(self, message):
        """
        Delivers a message to the Agent, and returns the response.

        If the send operation times out, or the response indicates a fatal error,
        an error message is displayed and the console terminates with a status
        code of -1.
        """

        try:
            message = self.__server.sendAndReceive(message.setSessionId(self.__session_id))
        except socket.timeout:
            self.stderr.write("lost session: %s\n"%self.__session_id)

            sys.exit(-1)

        if message and message.type == Message.REFLECTION_RESPONSE and message.reflection_response.status == Message.ReflectionResponse.FATAL:
            self.stderr.write("lost session: %s\n"%self.__session_id)

            sys.exit(-1)

        return message

    def __module(self, key):
        """
        Gets a module instance, by identifier, and initialises it with the
        required session parameters.
        """

        module = None

        try:
            module = Module.get(self.__module_name(key))
        except KeyError:
            pass

        if module == None:
            try:
                module = Module.get(key)
            except KeyError:
                pass

        if module == None:
            raise KeyError(key)
        else:
            return module(self.__reflector, self.stdout, self.stderr)

    def __module_name(self, key):
        """
        Decodes a full module identifier, given a user's input.

        This helps to find modules after the user has changed namespace.
        """

        if key.startswith("."):
            return key[1:]
        elif self.__base == "":
            return key
        else:
            return self.__base + key

    def __modules(self):
        """
        Gets a full list of all module identifiers.
        """

        if self.__base == "":
            return Module.all()
        else:
            return filter(lambda m: m.startswith(self.__base), Module.all())

    def __namespaces(self, global_scope=False):
        """
        Gets a full list of all namespace identifiers, either globally or in
        the current namespace scope.
        """

        if global_scope:
            return set(map(lambda m: self.__module("." + m).namespace(), Module.all()))
        else:
            return set(map(lambda m: self.__module("." + m).namespace(), self.__modules()))

    def __setBase(self, base):
        """
        Changes the user's namespace.

        Changing to:

            'str' - selects the 'str' namespace, within the currently active
                    namespace
           '.str' - selects the 'str' namespace, in the root namespace
             '..' - goes back on namespace
               '' - goes back to the root namespace
        """

        if base == "":
            self.__base = base
        else:
            if base == "..":
                path = self.__base.split(".")

                try:
                    path.pop(-2)
                except IndexError:
                    pass

                target = ".".join(path)
            elif base.startswith("."):
                target = base[1:] + "."
            else:
                target = self.__base + base + "."

            if True in map(lambda m: m.startswith(target), Module.all()):
                self.__base = target
            else:
                self.stderr.write("no such namespace: %s\n"%base)

        if base == "":
            self.prompt = "mercury> "
        else:
            self.prompt = "mercury#{}> ".format(self.__base[0:len(self.__base)-1])

        return True

class DebugSession(Session):
    """
    DebugSession is a subclass of Session, which rewrites the default error
    handlers to print stacktrace information.
    """

    def __init__(self, server, session_id):
        Session.__init__(self, server, session_id)

        self.intro = "Mercury Console (debug mode)"
        self.prompt = "mercury> "
        
    def do_reload(self, args):
        """
        usage: reload
        
        Load a fresh copy of all modules from disk.
        """
        
        Module.reload()
        
        print "Done.\n"

    def handleException(self, e):
        """
        Invoked whenever an exception is triggered by a module, to handle the
        throwable and display some information to the user.
        """

        self.stderr.write("exception in module: {}: {}\n".format(e.__class__.__name__, str(e)))
        self.stderr.write("%s\n"%traceback.format_exc())
