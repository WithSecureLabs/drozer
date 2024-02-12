import sys

class MockSession(object):
    
    def __init__(self, reflector, stdout=sys.stdout, stderr=sys.stderr, variables={}):
        self.__reflector = reflector
        self.stdout = stdout
        self.stderr = stderr
        self.variables = variables
    
    def get_reflector(self):
        return self.__reflector
        