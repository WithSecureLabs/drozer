from xml.etree import ElementTree

from drozer.modules.common import assets, loader

class IntentFilter(assets.Assets, loader.ClassLoader):
    """
    This drozer module mixin provides features for extracting Intent Filters
    for IPC endpoints, by parsing the AndroidManifest.xml file.
    """

    __filter_xpath = "./application/%s[@name='%s']/intent-filter"

    def find_intent_filters(self, endpoint, endpoint_type):
        filters = set([])

        xml = ElementTree.fromstring(self.getAndroidManifest(endpoint.packageName))

        filters.update(map(self.__parse_filter, xml.findall(self.__filter_xpath % (endpoint_type, str(endpoint.name)[len(endpoint.packageName):]))))
        filters.update(map(self.__parse_filter, xml.findall(self.__filter_xpath % (endpoint_type, str(endpoint.name)[len(endpoint.packageName)+1:]))))
        filters.update(map(self.__parse_filter, xml.findall(self.__filter_xpath % (endpoint_type, str(endpoint.name)))))
        
        return filters

    def __parse_filter(self, element):
        intent_filter = IntentFilter.Filter()
        
        for child in element.getchildren():
            if child.tag == "action":
                intent_filter.add_action(child.attrib['name'])
            elif child.tag == "category":
                intent_filter.add_category(child.attrib['name'])
            elif child.tag == "data":
                intent_filter.add_data(IntentFilter.Data.from_attributes(child.attrib))
        
        return intent_filter


    class Data(object):

        def __init__(self, scheme=None, host=None, port=None, path=None, mimetype=None):
            self.scheme = scheme
            self.host = host
            self.port = port
            self.path = path
            self.mimetype = mimetype

        @classmethod
        def from_attributes(cls, attrs):
            scheme = 'scheme' in attrs and attrs['scheme']
            host = 'host' in attrs and attrs['host']
            port = 'port' in attrs and attrs['port']
            path = 'path' in attrs and attrs['path']
            mimetype = 'mimeType' in attrs and attrs['mimeType']

            return cls(scheme, host, port, path, mimetype)

        def __str__(self):
            return "%s://%s:%s%s (type: %s)" % (self.scheme or "*", self.host or "*", self.port or "*", self.path or "*", self.mimetype or "*")


    class Filter(object):

        def __init__(self):
            self.actions = []
            self.categories = []
            self.datas = []

        def add_action(self, action):
            self.actions.append(action)

        def add_category(self, category):
            self.categories.append(category)

        def add_data(self, data):
            self.datas.append(data)

