
class Transport(object):
    
    def __init__(self):
        self.__id = 1
        
    def nextId(self):
        """
        Calculates the next Message identifier for this connection.
        """

        self.__id += 1

        return self.__id
        