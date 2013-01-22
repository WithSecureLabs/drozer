import binascii
import hashlib
import os

from mwr.cinnibar.reflection.types import ReflectedPrimitive
from mwr.cinnibar.reflection.utils import ClassBuilder
from mwr.common import fs

from mwr.droidhg.modules.base import Module

class ClassLoader(object):
    """
    Mercury Client Module: provides utility methods for loading Java source code
    from the local system into the Dalvik VM on the Agent.
    """

    def getClassLoader(self, source_or_relative_path, relative_to=None):
        """
        Gets a DexClassLoader on the agent, given compiled source or an apk
        file from the local system.
        """

        source = self.__getSource(source_or_relative_path, relative_to=relative_to)

        if source != None:
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
        else:
            raise RuntimeError("Mercury could not find or compile the extension library %s.\n" % os.path.basename(source_or_relative_path))

    def loadClass(self, source, klass, relative_to=None):
        """
        Load a Class from a local apk file (source) on the running Dalvik VM.
        """
        
        if not Module.cached_klass(".".join([source, klass])):
            Module.cache_klass(".".join([source, klass]), self.getClassLoader(source, relative_to=relative_to).loadClass(klass))
            
        return Module.get_cached_klass(".".join([source, klass]))

    def __getCachePath(self):
        """
        Get a working path, to which the compiled will be unpacked.
        """

        return self.getContext().getCacheDir().getAbsolutePath().native()

    def __getSource(self, source_or_relative_path, relative_to=None):
        """
        Get source, either from an apk file or passed directly.
        """
        
        source = None

        if source_or_relative_path.endswith(".apk"):
            if relative_to == None:
                relative_to = os.path.join(os.path.dirname(__file__), "..")
            elif relative_to.find(".py") >= 0 or relative_to.find(".pyc") >= 0:
                relative_to = os.path.dirname(relative_to)
                
            apk_path = os.path.join(relative_to, *source_or_relative_path.split("/"))
            java_path = apk_path.replace(".apk", ".java")
            
            if os.path.exists(apk_path):
                source = fs.read(apk_path)
            elif os.path.exists(java_path):
                source = ClassBuilder(java_path).build()
        else:
            source = source_or_relative_path

        return source
