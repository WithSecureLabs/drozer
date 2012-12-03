import functools
import urlparse

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from mwr.droidhg.modules import common, Module
from mwr.droidhg.reflection import ReflectionException

class WebContentResolver(Module, common.PackageManager, common.Provider):

    name = "Start a Web Service interface to Content Providers."
    description = "Start a Web Service interface to Content Providers. This allows you to use web application testing capabilities and tools to test content providers."
    examples = """mercury> run auxiliary.webcontentresolver

    WebContentResolver started on port 8080.
    Ctrl+C to Stop"""
    author = "Nils (@mwrlabs)"
    date = "2012-11-06"
    license = "MWR Code License"
    path = ["auxiliary"]

    def add_arguments(self, parser):
        parser.add_argument("port", default=8080, help="the port to start the WebContentResolver on", nargs='?')
    
    def execute(self, arguments):
        try:
            server = HTTPServer(('', int(arguments.port)), functools.partial(Handler, self))

            print "WebContentResolver started on port " + str(arguments.port) + "."
            print "Ctrl+C to Stop"

            server.serve_forever()
        except KeyboardInterrupt:
            print "Stopping...\n"

            server.socket.close()

class Handler(BaseHTTPRequestHandler):

    header = """<html><head><title>Mercury WebContentResolver</title><style type="text/css">body { font-family: "Lucida Grande", Verdana, Arial, Helvetica, sans-serif; font-size: 12px; } table { font-size: inherit; }</style></head><body><h1>Mercury WebContentResolver</h1>\n"""
    footer = """</body></html>"""

    def __init__(self, module, *args, **kwargs):
        self.module = module

        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        url = urlparse.urlparse(self.path)

        path = [ x for x in url.path.split('/') if x ]

        params = urlparse.parse_qs(url.query)
        request = {}

        try:
            if not path or path[0] == 'list':
                # TODO: support filter/permissions params 
                #for param in ['filter', 'permissions']:
                #    request[param] = params.get(param, [None])[0]

                output = self.__provider_list()

                self.wfile.write(self.header + output + self.footer)
            elif path[0] == 'query':
                # TODO: apply projection, selection, selectionArgs, sortOrder, showColumns
                #for param in ['uri', 'projection', 'selection', 'selectionArgs', 'sortOrder', 'showColumns']:
                #    request[param] = params.get(param, [None])[0]

                output = self.__query(params.get('uri', [None])[0], params.get('projection', [None])[0], params.get('selection', [None])[0], params.get('selectionArgs', [None])[0], params.get('selectionSort', [None])[0])

                self.wfile.write(self.header + output + self.footer)
            else:
                self.wfile.write(self.header + self.usage() + self.footer)
        except ReflectionException as e:
            self.wfile.write(self.header + self.__format_exception(e) + self.footer)

    def __format_exception(self, e):
        return "<h1>" + str(e.__class__) + "</h1><p>" + e.message + "</p>"

    def __provider_list(self):
        output = """<table><tr><th>Package</th>
                               <th colspan="2">Authorities</th>
                               <th>Read permission</th>
                               <th>Write permission</th>
                               <th>Multipermission</th></tr>
                            """

        def link(path, display):
            return "<a href='%s'>%s</a>" % (path, display)

        def linkcontent(url, display=None):
            return link("/query?uri=content://%s&projection=&selection=&selectionSort=&showColumns=" % url, display or url)

        def linkfilter(url, display=None):
            return link("/?filter=%s" % url, display or url)

        def linkperm(url, display=None):
            return link("/?permissions=%s" % url, display or url)

        for package in self.module.packageManager().getPackages(common.PackageManager.GET_PROVIDERS):
            if package.providers != None:
                for provider in package.providers:

                    # Give the general values first
                    authorities = provider.authority.split(";")
                    output += "<tr><td>%s</td>" % linkfilter(provider.packageName)
                    output += "<td colspan='2'>%s</td>" % "<br/>".join([linkcontent(a) for a in authorities])
                    output += "<td>%s</td>" % linkperm(provider.readPermission)
                    output += "<td>%s</td>" % linkperm(provider.writePermission)
                    output += "<td>%s</td></tr>" % provider.multiprocess

                    if provider.pathPermissions != None:
                        for permission in provider.pathPermissions:
                            output += "<tr><td>&nbsp;</td><td>&nbsp;</td>"
                            output += "<td>%s</td>" % linkcontent("%s%s" % (authorities[0], permission.getPath()), permission.getPath())
                            output += "<td>%s</td>" % linkperm(permission.getReadPermission())
                            output += "<td>%s</td>" % linkperm(permission.getReadPermission())
                            output += "<td>&nbsp;</td></tr>"
        output += "</table>"
        return output

    def __query(self, uri, projection=None, selection=None, selectionArgs=None, sortOrder=None):
        cursor = self.module.contentResolver().query(uri, projection != None and projection.split(",") or None, selection, selectionArgs != None and selectionArgs.split(",") or None, sortOrder)
        output = "<table><thead><tr>"

        if cursor != None:
            rows = self.module.getResultSet(cursor)

            for i in range(len(rows[0])):
                output += "<th>%s</th>" % rows[0][i]
            
            output += "</tr></thead><tbody>"
            
            for r in rows[1:]:
                output += "<tr>"
                for i in range(len(r)):
                    output += "<td>%s</td>" % r[i]
                output += "</tr>"

            output += "</tbody></table>"
            
            return output
        else:
            return "Unable to query %s." % uri

    def usage(self):
        return """
<p>Usage instructions:</p>

<ul>
<li>To access a list of providers:
  <a href="http://localhost:8080/list">http://localhost:8080/providers</a></li>

<li>To access a particular provider:
  http://localhost:8080/query?projection=<projection>&selection=<selection>&selectionArgs=<selectionArgs>&sortOrder=</li>
</ul>
"""
