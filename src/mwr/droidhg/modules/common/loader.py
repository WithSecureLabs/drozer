import binascii
import hashlib
import os

from mwr.droidhg.modules.base import Module
from mwr.droidhg.reflection import ReflectedPrimitive

class ClassLoader(object):
    """
    Mercury Client Module: provides utility methods for loading Java source code
    from the local system into the Dalvik VM on the Agent.
    """

    def getClassLoader(self, source_or_relative_path):
        """
        Gets a DexClassLoader on the agent, given compiled source or an apk
        file from the local system.
        """
        
        source = self.__getSource(source_or_relative_path)

        path = self.__getCachePath()
        file_name = binascii.hexlify(hashlib.md5(source).digest()) + ".apk"
        file_path = "/".join([path, file_name])

        file_io = self.new("java.io.File", file_path)

        if file_io.exists() != True or file_io.length() != len(source):
            source_data = [ReflectedPrimitive("byte", (ord(i) if ord(i) < 128 else ord(i) - 0x100), reflector=self.reflector()) for i in source]

            file_stream = self.new("java.io.FileOutputStream", file_path)
            file_stream.write(source_data, 0, len(source_data))
            file_stream.close()
        
        return self.new('dalvik.system.DexClassLoader', file_path, path, None, self.klass('java.lang.ClassLoader').getSystemClassLoader())

    def loadClass(self, source, klass):
        """
        Load a Class from a local apk file (source) on the running Dalvik VM.
        """
        
        if not ".".join([source, klass]) in Module._Module__klasses:
            Module._Module__klasses[".".join([source, klass])] = self.getClassLoader(source).loadClass(klass)
            
        return Module._Module__klasses[".".join([source, klass])]

    def __getCachePath(self):
        """
        Get a working path, to which the compiled will be unpacked.
        """

        return self.getContext().getCacheDir().getAbsolutePath().native()

    def __getSource(self, source_or_relative_path):
        """
        Get source, either from an apk file or passed directly.
        """

        if source_or_relative_path.endswith(".apk"):
            apk_path = os.path.join(os.path.dirname(__file__), "..", *source_or_relative_path.split("/"))
            
            file_handle = open(apk_path, 'rb')
            data = file_handle.read()
            source = data
            
            while data != "":
                data = file_handle.read()
                source += data

            file_handle.close()
        else:
            source = source_or_relative_path

        return source
