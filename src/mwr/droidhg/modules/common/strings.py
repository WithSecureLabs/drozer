class Strings(object):
    """
    Mercury Client Library: provides an implementation of the *nix `strings`
    command, which searches for ASCII strings in a specified file.
    """

    def getStrings(self, path):
        """
        Searches a file for Strings, and returns them in an Array.
        """

        StringsKlass = self.klass("com.mwr.droidhg.util.Strings")

        return StringsKlass.get(path).split("\n")
        