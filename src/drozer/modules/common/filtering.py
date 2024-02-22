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
            # yaynoteyay
            # i guess in python2, the length of a `filter` class could be obtained via `len(), but i guess this doesn't work in python3`
            # so making this return a `list` instead of `filter`
            return list(filter(lambda e: str(getattr(e, key)).upper().find(str(term).upper()) >= 0, collection))
        else:
            return collection
