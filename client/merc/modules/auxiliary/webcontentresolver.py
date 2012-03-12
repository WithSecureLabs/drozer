from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from merc.lib.modules import Module
import urlparse

import functools

class Handler(BaseHTTPRequestHandler):

    header = """<html><head><title>Mercury WebContentResolver</title></head><body><h1>Mercury WebContentResolver</h1>\n"""
    footer = """</body></html>"""

    def __init__(self, session, *args, **kwargs):
        self.session = session
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_GET(self):

        self.send_response(200)
        self.end_headers()

        url = urlparse.urlparse(self.path)
        path = [ x for x in url.path.split('/') if x ] #pylint: disable-msg=E1101

        params = urlparse.parse_qs(url.query) #pylint: disable-msg=E1101
        request = {}

        if not path or path[0] == 'list':
            for param in ['filter', 'permissions']:
                request[param] = params.get(param, [None])[0]

            result = self.session.executeCommand("provider", "info", request)
            output = self.html_provider_list(result)

            self.wfile.write(self.header + output + self.footer)
            return

        elif path[0] == 'query':
            for param in ['uri', 'projection', 'selection', 'selectionArgs', 'sortOrder', 'showColumns']:
                request[param] = params.get(param, [None])[0]

            self.wfile.write(self.session.executeCommand("provider", "query", request).getErrorOrData())
            return

        # Fall back to printing the usage message
        self.wfile.write(self.usage())
        return

    def html_provider_list(self, result):
        """ Returns an HTML table of a provider list"""
        if result.error:
            return result.error

        # Split apart the result into individual providers
        providers = result.data.split("\n\n")

        # Build up a provider datastructure
        processed = []
        for p in providers:
            pdict = {}
            for value in p.split("\n"):
                i = value.find(':')
                if value.startswith('Path Permission') or value.startswith('URI Permission'):
                    permlist = pdict.get(value[:i], [])
                    permlist.append(value[i + 2:])
                    pdict[value[:i]] = permlist
                else:
                    pdict[value[:i]] = value[i + 2:]

            # In case we got one that didn't process correctly
            if pdict.get('Authority', None):
                processed.append(pdict)

        output = """<table style="{width:100%}"><tr><th>Package</th>
                               <th colspan="2">Authorities</th>
                               <th>Read permission</th>
                               <th>Write permission</th>
                               <th>URI Permission</th>
                               <th>Multipermission</th></tr>
                            """

        def link(path, display):
            return "<a href='" + path + "'>" + display + "</a>"

        def linkcontent(url, display = None):
            return link("http://localhost:8080/query?uri=content://" + url + "&projection=&selection=&selectionSort=&showColumns=", display or url)

        def linkfilter(url, display = None):
            return link("http://localhost:8080/?filter=" + url, display or url)

        def linkperm(url, display = None):
            return link("http://localhost:8080/?permissions=" + url, display or url)

        for p in sorted(processed, key = lambda x: x.get('Package name', '')):
            # Give the general values first
            authorities = p.get('Authority', '').split(';')
            output += "<tr><td>" + linkfilter(p.get('Package name', '')) + "</td>"
            output += "<td colspan='2'>" + "<br>".join([linkcontent(x) for x in authorities]) + "</td>"
            output += "<td>" + linkperm(p.get('Required Permission - Read', '')) + "</td>"
            output += "<td>" + linkperm(p.get('Required Permission - Write', '')) + "</td>"
            output += "<td>" + "<br>".join([linkcontent(authorities[0] + x, x) for x in p.get('URI Permission Pattern', '')]) + "</td>"
            output += "<td>" + p.get('Multiprocess allowed', '') + "</td></tr>"

            # Separate the path permissions out into type
            pathperms = {}
            for perm in ['Read', 'Write']:
                for permission in p.get('Path Permission - ' + perm, ''):
                    permarray = permission.split(" needs ")
                    if len(permarray) > 1:
                        # Populate it if we've not seen the path before empty
                        pathperms[permarray[0]] = pathperms.get(permarray[0], {'Read': [], 'Write':[]})
                        pathperms[permarray[0]].get(perm).append(permarray[1])

            for path in pathperms.keys():
                output += "<tr><td>&nbsp;</td><td>&nbsp;</td>"
                output += "<td>" + linkcontent(authorities[0] + path, path) + "</td>"
                output += "<td>" + "<br>".join([linkperm(x) for x in pathperms[path]['Read']]) + "</td>"
                output += "<td>" + "<br>".join([linkperm(x) for x in pathperms[path]['Write']]) + "<td>"
                output += "<td colspan='2'>&nbsp;</td></tr>"
        output += "</table>"
        return output

    def usage(self):
        return self.header + """
<p>Usage instructions:</p>

<ul>
<li>To access a list of providers:
  <a href="http://localhost:8080/list">http://localhost:8080/providers</a></li>

<li>To access a particular provider:
  http://localhost:8080/query?projection=<projection>&selection=<selection>&selectionArgs=<selectionArgs>&sortOrder=&showColumns=</li>
</ul>
""" + self.footer

class WebContentResolver(Module):
    """Note: THIS IS INCOMPLETE - FULL VERSION STILL TO COME
Description: Provides a web service interface to Android content providers, in order to use web application testing capabilities and tools to test content providers.
Credit: Nils - MWR Labs"""

    def __init__(self, *args, **kwargs):
        Module.__init__(self, *args, **kwargs)
        self.path = ["auxiliary"]

    def execute(self, session, _arg):

        try:
            port = 8080
            server = HTTPServer(('', port), functools.partial(Handler, session))
            print "\nWebcontentresolver started on port " + str(port)
            print "Control + c to stop"
            server.serve_forever()

        except KeyboardInterrupt:
            print "Stopping...\n"
            server.socket.close()
