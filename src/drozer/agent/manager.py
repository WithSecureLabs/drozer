import itertools
from mwr.common import cli

from drozer import android, meta
from drozer.agent import builder, manifest

class AgentManager(cli.Base):
    """
    drozer agent COMMAND [OPTIONS]
    
    A utility for building custom drozer Agents.
    """
    
    def __init__(self):
        cli.Base.__init__(self)
        
        self._parser.add_argument("--rogue", action="store_true", default=False, help="create a rogue agent with no GUI")
        self._parser.add_argument("--no-gui", action="store_true", default=False, help="deprecated: rather use --rogue. create an agent with no GUI")
        self._parser.add_argument("--granular", action="store_true", default=False, help="don't request all permissions when building GUI-less agent")
        self._parser.add_argument("--permission", "-p", nargs="+", help="add permissions to the Agent manifest")
        self._parser.add_argument("--define-permission", "-d", metavar="name protectionLevel", nargs="+", help="define a permission and protectionLevel in the Agent manifest")
        self._parser.add_argument("--server", default=None, metavar="HOST[:PORT]", help="specify the address and port of the drozer server")
        
    def do_build(self, arguments):
        """build a drozer Agent"""

        source = (arguments.rogue or arguments.no_gui) and "rogue-agent" or "standard-agent"
        packager = builder.Packager()
        packager.unpack(source)
        
        if arguments.rogue or arguments.no_gui:
            e = manifest.Endpoint(packager.endpoint_path())
            if arguments.server != None:
                e.put_server(arguments.server)
            e.write()
            
            if not arguments.granular:
                permissions = set(android.permissions)
            else:
                permissions = set([])
        else:
            permissions = set([])
        
        if arguments.permission != None:
            permissions = permissions.union(arguments.permission)

        defined_permissions = {}
        if arguments.define_permission != None:
            defined_permissions = dict(itertools.izip_longest(*[iter(arguments.define_permission)] * 2, fillvalue=""))

        # add extra permissions to the Manifest file
        m = manifest.Manifest(packager.manifest_path()) 
        
        m_ver = m.version()
        c_ver = meta.version.__str__()

        if m_ver != c_ver:
            print "Version Mismatch: Consider updating your build(s)"
            print "Agent Version: %s" % m_ver
            print "drozer Version: %s" % c_ver

        for p in permissions:
            m.add_permission(p)

        for name, protectionLevel in defined_permissions.iteritems():
            m.define_permission(name, protectionLevel)

        m.write()

        built = packager.package()
        
        print "Done:", built
