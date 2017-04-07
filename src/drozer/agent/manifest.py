from xml.etree import ElementTree as xml

class Endpoint(object):
    
    def __init__(self, path):
        self.__path = path
        
        lines = open(self.__path).read().split("\n")
        data = dict(map(lambda l: l.split(":"), filter(lambda l: l.find(":") > -1, lines)))
        
        self.host = data['host']
        self.password = data['password']
        self.port = int(data['port'])
        self.ssl = data['ssl'].startswith("t")
        self.ts_password = data['ts_password']
        self.ts_path = data['ts_path']
    
    def put_server(self, server):
        if isinstance(server, tuple):
            self.host, self.port = server
        else:
            if server.find(":") > -1:
                self.host, self.port = server.split(":")
            else:
                self.host = server
    
    def write(self):
        h = open(self.__path, 'w')

        h.write("drozer Endpoint\n")
        h.write("---------------\n")
        h.write("host:" + self.host + "\n")
        h.write("port:" + str(self.port) + "\n")
        h.write("password:" + self.password + "\n")
        h.write("ssl:" + str(self.ssl).lower() + "\n")
        h.write("ts_path:" + self.ts_path + "\n")
        h.write("ts_password:" + self.ts_password)


class Manifest(object):
    
    def __init__(self, path):
        self.__path = path
        self.__doc = xml.fromstring(file(self.__path).read())
        
    
    def add_permission(self, name):
        node = xml.Element('uses-permission')
        node.attrib["ns0:name"] = name
        
        self.__doc.insert(len(self.__doc.getchildren()) - 1, node)

    def define_permission(self, name, protectionLevel):
        node = xml.Element('permission')
        node.attrib["ns0:name"] = name
        node.attrib["ns0:protectionLevel"] = protectionLevel
        
        self.__doc.insert(len(self.__doc.getchildren()) - 1, node)
        
    def permissions(self):
        return self.__doc.findall('uses-permission')

    def write(self):
        xml.ElementTree(self.__doc).write(self.__path)

    def version(self):
        return self.__doc.attrib['{http://schemas.android.com/apk/res/android}versionName']
        
