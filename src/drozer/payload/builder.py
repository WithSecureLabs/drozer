import os
import shutil

from mwr.common import command_wrapper, system

from drozer.configuration import Configuration

class Packager(command_wrapper.Wrapper):
    
    __ant = Configuration.executable("ant")
    
    __manifest = "AndroidManifest.xml"
    
    def __init__(self):
        self.__wd = self._get_wd()
    
    def copy_sources_from(self, name):
        shutil.copytree(os.path.join(Configuration.library(name)), os.path.join(self.__wd, "agent"))
        shutil.copytree(os.path.join(Configuration.library("jdiesel")), os.path.join(self.__wd, "jdiesel"))
        shutil.copytree(os.path.join(Configuration.library("mwr-tls")), os.path.join(self.__wd, "mwr-tls"))
    
    def endpoint_path(self):
        return os.path.join(self.__wd, "agent", "res", "raw", "endpoint.txt")
    
    def manifest_path(self):
        return os.path.join(self.__wd, "agent", "AndroidManifest.xml")
    
    def package(self):
        cwd = os.getcwd()
        os.chdir(os.path.join(self.__wd, "agent"))
        
        if self._execute([self.__ant, "debug"]) != 0:
            raise RuntimeError("failed to build")
        
        os.chdir(cwd)
        
        return os.path.join(self.__wd, "agent", "bin", "agent-debug.apk")
