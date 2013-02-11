import binascii
import hashlib
import os, md5

from mwr.cinnibar.reflection.types import ReflectedPrimitive
from mwr.cinnibar.reflection.utils import ClassBuilder
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
    
            #if file_io.exists() != True or file_io.length() != len(self.source):
            if self.__verify_file(file_io, self.source):
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
        calulates the md5 of the local and remote files
        and checks that they are equal
        
        remote: a java File object that points to the apk in question
        local : the local apk (console side) source data
        """     

        
        """no point checking if the file does not exists!"""
        if remote == None or remote.exists() == False:
            return False;
        print "constructing byte array"
        remote_data = ""
        print "constructing inpustream"
        remote_file = self.construct("java.io.FileInputStream", remote)
        print "getting data, remote length %d" %remote.length()

        """
        while remote_file.read(remote_data, 0, remote.length()) != -1:
            pass
        """
        for i in range(0, remote.length()):
            remote_data += chr(remote_file.read())
        
        print "remote_data length: %d"%len(remote_data)
        """
        the byte array is in a wierd format that we cannot use yet, the data must be reformatted in the system 
        """

        #print "remote_data: %s"%remote_data            
        print "remote_data length: %d"%len(remote_data)       
        
        a = md5.new(remote_data)
        b = md5.new(local_data)

        print "remote_data: %s"%remote_data
        print "local_data: %s" %local_data

        print ("a: %s, b:%s" %(a.digest(),b.digest()))

        match = (a.digest() == b.digest())
        
        print "match: %s" % match
        return a.digest() == b.digest()
        
           
        
