import binascii
import hashlib
import os, md5

from pydiesel.reflection.exceptions import ReflectionException
from pydiesel.reflection.types.reflected_primitive import ReflectedPrimitive
from pydiesel.reflection.utils import ClassBuilder
from mwr.common import fs

class ClassLoader(object):
    """
    Mercury Client Module: provides utility methods for loading Java source code
    from the local system into the Dalvik VM on the Agent.
    """
    
    def __init__(self, source_or_relative_path, cache_path, construct, system_class_loader, relative_to=None):
        self.source = self.__get_source(source_or_relative_path, relative_to=relative_to)
        
        self.cache_path = cache_path
        self.construct = construct
        self.system_class_loader = system_class_loader

    def loadClass(self, klass):
        return self.getClassLoader().loadClass(klass);
        
    def getClassLoader(self):
        """
        Gets a DexClassLoader on the agent, given compiled source or an apk
        file from the local system.
        """

        if self.source != None:
            file_path = "/".join([self.cache_path, self.__get_cached_apk_name()])
    
            file_io = self.construct('java.io.File', file_path)
            
            if not self.__verify_file(file_io, self.source):  
                source_data = [ReflectedPrimitive("byte", (ord(i) if ord(i) < 128 else ord(i) - 0x100), reflector=None) for i in self.source]
    
                file_stream = self.construct("java.io.FileOutputStream", file_path)
                file_stream.write(source_data, 0, len(source_data))
                file_stream.close()
            return self.construct('dalvik.system.DexClassLoader', file_path, self.cache_path, None, self.system_class_loader)
        else:
            raise RuntimeError("Mercury could not find or compile a required extension library.\n")

    def __get_cached_apk_name(self):
        """
        Calculate a unique name for the cached APK file, based on the content
        of the library file.
        """
        
        return binascii.hexlify(hashlib.md5(self.source).digest()) + ".apk"
    
    def __get_source(self, source_or_relative_path, relative_to=None):
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

    def __verify_file(self, remote, local_data):
        """
        checks the hash value of the requested apk to the one already present on the agent
        """

        if remote == None or not remote.exists() or local_data == None:
            """
            no file present on the agent
            """
            return False
        
        remote_hash = ""        
        try:
            remote_verify = self.construct("com.mwr.droidhg.util.Verify")
            remote_hash = remote_verify.md5sum(remote)
        except ReflectionException:
            """
            this means that the agent does not have the hash function
            """
            
            print
            print "   +------------------------------------------------------------------------+   "
            print "   | Mercury needs to upload some additional code to run this module. The   |   "
            print "   | code seems to have already been uploaded, but Mercury cannot verify it |   "
            print "   | because you seem to be running an old version of the Mercury Agent.    |   "
            print "   |                                                                        |   "
            print "   | Mercury can perform this verification locally, but this is typically   |   "
            print "   | very slow.                                                             |   "
            print "   |                                                                        |   "
            print "   | Would you like to verify the remote file? [yN]                         |   "
            print "   +------------------------------------------------------------------------+   "
            
            if(raw_input().lower() == 'y'):
                remote_hash = self.__local_md5sum(remote)
            else:
                print "   +------------------------------------------------------------------------+   "
                print "   | Skipping Verification.                                                 |   "
                print "   +------------------------------------------------------------------------+   "
                print
                
                return True
            
        local_hash = md5.new(local_data).digest().encode("hex")
        
        return remote_hash == local_hash

    def __local_md5sum(self, remote):
        """
        this is really, really slow
        typically ~100b a second
        """
        remote_data = ""
        remote_file = self.construct("java.io.FileInputStream", remote)
        
        # read the file back from the Agent, one byte at a time
        for i in range(0, remote.length()):
            remote_data += chr(remote_file.read())
        
        return md5.new(remote_data).digest().encode("hex")
        