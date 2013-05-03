class Filters(object):
    """
    Utility methods for filtering collections of ReflectedTypes.
    """

    def match_filter(self, collection, key, term):
        """
        Implements a filter for items in collection, where the value of the
        property 'key' is equal to 'term'.
        """

        if collection == None:
            collection = []
            
        if term != None and term != "":
            return filter(lambda e: str(getattr(e, key)).upper().find(str(term).upper()) >= 0, collection)
        else:
            return collection
