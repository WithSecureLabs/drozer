from pydiesel.api.protobuf_pb2 import Message
from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_type import ReflectedType

class ReflectedString(ReflectedType):
    """
    A ReflectedType that represents a String.
    """
    
    def __init__(self, native, *args, **kwargs):
        ReflectedType.__init__(self, *args, **kwargs)
        
        try:
            self._native = native.decode("utf-8")
        except UnicodeError:
            self._native = native

    def capitalize(self):
        """
        Return a copy of word with only its first character capitalized.
        """

        return self._native.capitalize()

    def center(self, width, fillchar=" "):
        """
        Center a string in a field of given width.
        """

        return self._native.center(width, fillchar)

    def count(self, sub, start=0, end=-1):
        """
        Return the number of non-overlapping occurrences of substring sub in the
        range [start, end]. Optional arguments start and end are interpreted as
        in slice notation.
        """

        return self._native.count(sub, start, end)

    def endswith(self, suffix, start=0, end=None):
        """
        Return True if the string ends with the specified suffix, otherwise return
        False. suffix can also be a tuple of suffixes to look for. With optional
        start, test beginning at that position. With optional end, stop comparing
        at that position.
        """

        return self._native.endswith(suffix, start, end == None and len(self._native) or end)

    def expandtabs(self, tabsize=8):
        """
        Return a copy of the string where all tab characters are replaced by one
        or more spaces, depending on the current column and the given tab size.
        The column number is reset to zero after each newline occurring in the
        string. If tabsize is not given, a tab size of 8 characters is assumed.
        This doesn't understand other non-printing characters or escape sequences.
        """

        return self._native.expandtabs(tabsize)

    def find(self, sub, start=0, end=-1):
        """
        Return the lowest index in the string where substring sub is found,
        such that sub is contained in the slice s[start:end]. Optional
        arguments start and end are interpreted as in slice notation. Return
        -1 if sub is not found.
        """

        return self._native.find(sub, start, end)

    def format(self, *attrs):
        """
        Perform a string formatting operation.
        """

        return self._native.format(*attrs)

    def index(self, sub, start=0, end=-1):
        """
        Like find(), but raise ValueError when the substring is not found.
        """

        return self._native.index(sub, start, end)

    def isalnum(self):
        """
        Return true if all characters in the string are alphanumeric and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isalnum()

    def isalpha(self):
        """
        Return true if all characters in the string are alphabetic and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isalpha()

    def isdigit(self):
        """
        Return true if all characters in the string are digits and there
        is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isdigit()

    def islower(self):
        """
        Return true if all cased characters [4] in the string are lowercase and
        there is at least one cased character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.islower()

    def isspace(self):
        """
        Return true if there are only whitespace characters in the string and
        there is at least one character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isspace()

    def istitle(self):
        """
        Return true if the string is a titlecased string and there is at least
        one character, for example uppercase characters may only follow uncased
        characters and lowercase characters only cased ones. Return false
        otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.istitle()

    def isupper(self):
        """
        Return true if all cased characters [4] in the string are uppercase and
        there is at least one cased character, false otherwise.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.isupper()

    def join(self, iterable):
        """
        Return a string which is the concatenation of the strings in the iterable
        iterable. The separator between elements is the string providing this
        method.
        """

        return self._native.join(map(lambda s: str(s), iterable))

    def ljust(self, width, fillchar=" "):
        """
        Return the string left justified in a string of length width. Padding
        is done using the specified fillchar (default is a space). The original
        string is returned if width is less than or equal to len(s).
        """

        return self._native.ljust(width, fillchar)

    def lower(self):
        """
        Return a copy of the string with all the cased characters converted to
        lowercase.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.lower()

    def lstrip(self, chars=None):
        """
        Return a copy of the string with leading characters removed. The chars
        argument is a string specifying the set of characters to be removed.
        If omitted or None, the chars argument defaults to removing whitespace.
        """

        return self._native.lstrip(chars)

    def native(self):
        """
        Get the native representation of the String.
        """

        return self._native

    def partition(self, sep):
        """
        Split the string at the first occurrence of sep, and return a 3-tuple
        containing the part before the separator, the separator itself, and
        the part after the separator. If the separator is not found, return
        a 3-tuple containing the string itself, followed by two empty strings.
        """

        return self._native.partition(sep)

    def replace(self, old, new, count=-1):
        """
        Return a copy of the string with all occurrences of substring old
        replaced by new. If the optional argument count is given, only the
        first count occurrences are replaced.
        """

        return self._native.replace(old, new, count)

    def rfind(self, sub, start=0, end=-1):
        """
        Return the highest index in the string where substring sub is found,
        such that sub is contained within s[start:end]. Optional arguments
        start and end are interpreted as in slice notation. Return -1 on
        failure.
        """

        return self._native.rfind(sub, start, end)

    def rindex(self, sub, start=0, end=-1):
        """
        Like rfind() but raises ValueError when the substring sub is not found.
        """

        return self._native.rindex(sub, start, end)

    def rjust(self, width, fillchar=" "):
        """
        Return the string right justified in a string of length width. Padding
        is done using the specified fillchar (default is a space). The original
        string is returned if width is less than or equal to len(s).
        """

        return self._native.rjust(width, fillchar)

    def rpartition(self, sep):
        """
        Split the string at the last occurrence of sep, and return a 3-tuple
        containing the part before the separator, the separator itself, and the
        part after the separator. If the separator is not found, return a 3-tuple
        containing two empty strings, followed by the string itself.
        """

        return self._native.rpartition(sep)

    def rsplit(self, sep=None, maxsplit=-1):
        """
        Return a list of the words in the string, using sep as the delimiter
        string. If maxsplit is given, at most maxsplit splits are done, the
        rightmost ones. If sep is not specified or None, any whitespace string
        is a separator. Except for splitting from the right, rsplit() behaves
        like split() which is described in detail below.
        """

        return self._native.rsplit(sep, maxsplit)

    def rstrip(self, chars=None):
        """
        Return a copy of the string with trailing characters removed. The chars
        argument is a string specifying the set of characters to be removed.
        If omitted or None, the chars argument defaults to removing whitespace.
        """

        return self._native.rstrip(chars)

    def split(self, *args, **kwargs):
        """
        Wrapper around the String#split method.
        """

        return self._native.split(*args, **kwargs)

    def splitlines(self, keepends=False):
        """
        Return a list of the lines in the string, breaking at line boundaries.
        This method uses the universal newlines approach to splitting lines.
        Line breaks are not included in the resulting list unless keepends is
        given and true.
        """

        return self._native.splitlines(keepends)

    def startswith(self, prefix, start=0, end=-1):
        """
        Return True if string starts with the prefix, otherwise return False.
        prefix can also be a tuple of prefixes to look for. With optional start,
        test string beginning at that position. With optional end, stop
        comparing string at that position.
        """

        return self._native.startswith(prefix, start, end)

    def strip(self, *args, **kwargs):
        """
        Wrapper around the String#strip method.
        """

        return self._native.strip(*args, **kwargs)

    def swapcase(self):
        """
        Return a copy of the string with uppercase characters converted to
        lowercase and vice versa.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.swapcase()

    def title(self):
        """
        Return a titlecased version of the string where words start with an
        uppercase character and the remaining characters are lowercase.

        The algorithm uses a simple language-independent definition of a word as
        groups of consecutive letters. The definition works in many contexts but
        it means that apostrophes in contractions and possessives form word
        boundaries, which may not be the desired result.

        For 8-bit strings, this method is locale-dependent.
        """

        return self._native.title()

    #def translate(self, table, deletechars=None)
    #    """
    #    Return a copy of the string where all characters occurring in the optional
    #    argument deletechars are removed, and the remaining characters have been
    #    mapped through the given translation table, which must be a string of
    #    length 256.
    #    """

    def upper(self):
        """
        Wrapper around the String#upper method.
        """

        return self._native.upper()

    def zfill(self, width):
        """
        Return the numeric string left filled with zeros in a string of length
        width. A sign prefix is handled correctly. The original string is returned
        if width is less than or equal to len(s).
        """

        return self._native.zfill(width)

    def _pb(self):
        """
        Get the Argument representation of the String, as defined in the drozer
        protocol.
        """

        return Message.Argument(type=Message.Argument.STRING, string=self._native)

    def __add__(self, other):
        return isinstance(other, ReflectedString) and self._native + other._native or self._native + other

    def __contains__(self, other):
        if isinstance(other, ReflectedString):
            return other._native in self._native
        else:
            return other in self._native

    def __eq__(self, other):
        return isinstance(other, ReflectedString) and self._native == other._native or self._native == other

    def __getitem__(self, key):
        return self._native[key]

    def __len__(self):
        return self._native.__len__()

    def __ne__(self, other):
        return isinstance(other, ReflectedString) and self._native != other._native or self._native != other

    def __repr__(self):
        return repr(self._native)

    def __str__(self):
        return self._native.encode('utf-8')
        