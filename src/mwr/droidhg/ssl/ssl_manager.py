from mwr.common import cli

class SSLManager(cli.Base):
    """
    mercury ssl {ca,keypair} [OPTIONS]
    
    Run the Mercury SSL Manager.

    The SSL Manager allows you to generate key material to enable TLS for your Mercury connections.
    """

    def __init__(self):
        cli.Base.__init__(self)
        
        self._parser.add_argument("type", choices=["ca", "keypair"], help="the type of key material to create")
    
    def do_create(self, arguments):
        """create some new key material"""
        
        print "creating", arguments.type
        