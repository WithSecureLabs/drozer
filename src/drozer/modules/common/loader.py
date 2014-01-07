import os, platform

from pydiesel.reflection import utils

from drozer.configuration import Configuration
from drozer.modules.base import Module

class ClassLoader(object):
    """
    Utility methods for loading Java source code from the local system into
    the Dalvik VM on the Agent.
    """

    def loadClass(self, source, klass, relative_to=None):
        """
        Load a Class from a local apk file (source) on the running Dalvik VM.
        """
        
        if relative_to == None:
            relative_to = os.path.join(os.path.dirname(__file__), "..")
        elif relative_to.find(".py") >= 0 or relative_to.find(".pyc") >= 0:
            relative_to = os.path.dirname(relative_to)
        
        if not Module.cached_klass(".".join([source, klass])):
            loader = utils.ClassLoader(source, self.__get_cache_path(), self.__get_constructor(), self.klass('java.lang.ClassLoader').getSystemClassLoader(), relative_to=relative_to)
            loader.android_path = lambda: Configuration.library("android.jar")
            loader.dx_path = lambda: Configuration.executable("dx.bat") if platform.system() == "Windows" else Configuration.executable("dx")
            loader.javac_path = lambda: Configuration.executable("javac")
            
            Module.cache_klass(".".join([source, klass]), loader.loadClass(klass))
            
        return Module.get_cached_klass(".".join([source, klass]))
     
    def __get_cache_path(self):
        """
        Get a working path, to which the compiled will be unpacked.
        """
        
        if self.has_context():
            # if context is available, we will read the cache directory from it
            return self.getContext().getCacheDir().getAbsolutePath().native()
        else:
            # otherwise, we must make a best effort guess
            return self.new("java.io.File", ".").getCanonicalPath().native()

    def __get_constructor(self):
        """
        Capture a reference to the default constructor (self.new) that can be
        passed as an argument.
        """
        
        def constructor(*args, **kwargs):
            return self.new(*args, **kwargs)
        
        return constructor
        
