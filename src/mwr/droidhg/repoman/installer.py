import os

from mwr.common import fs

class ModuleInstaller(object):
    
    def __init__(self, repository):
        self.repository = repository
    
    def install(self, modules):
        """
        Installs a list of modules, either as local or remote specs, and returns
        a dictionary of status information.
        """
        
        status = { 'success': [], 'fail': {} }

        for module in modules:
            print "Processing %s..." % module,
            
            try:
                self.__install_module(module)
                print "Done."
                
                status['success'].append(module)
            except InstallError as e:
                print "Failed."
                
                status['fail'][module] = str(e) 
        
        return status
    
    def __emit(self, path):
        """
        Write a blank file to a specified path.
        """
        
        fs.touch(path)
    
    def __ensure_packages(self, package):
        """
        Ensure that every directory between the repository root and a specified
        package contains an __init__.py file.
        """
        
        directories = package[len(self.repository):].split(os.path.sep)
        
        for i in range(len(directories)):
            self.__emit(os.path.join(self.repository, *directories[0:i+1] + ["__init__.py"]))

    def __install_module(self, module):
        """
        Install a module into a repository.
        """

        if module.find("/") >= 0 or module.find("\\") >= 0:
            source = self.__read_local_module(module)
        else:
            source = self.__read_remote_module(module)
        
        # check that we successfully read source for the module, otherwise there
        # isn't much more we can do here
        if source == None:
            raise InstallError("Failed to get module for '%s'." % module)
        
        return self.__unpack_module(os.path.basename(module), source)

    def __read_local_module(self, module):
        """
        Read a module file from the local filesystem, and return the source.
        """
        
        return fs.read(module)
    
    def __read_remote_module(self, module):
        """
        Read a module file from a remote, and return the source.
        """
        
        return None
    
    def __unpack_module(self, module, source):
        """
        Unpack some module source and install it into the repository. We may have:
        
          - raw python source; or
          - a zip file, containing several sources.
        
        We use the inferred path from the module name to create a package structure
        and either write Python source into the last segment, as a module, or
        unzip a zip file into that folder
        """
        
        # we assume the file is raw Python is we can read the package name that
        # Module should be imported from
        if source.find("mwr.droidhg.modules") >= 0:
            return self.__unpack_module_raw(module, source)
        else:
            print "zipped source"
            return False
        
        return True
    
    def __unpack_module_raw(self, module, source):
        """
        Handles unpacking a module and installing it, if the source is a Python
        module.
        """
        
        path = module.split(".")
        
        package = os.path.join(self.repository, *path[0:-1])
        # create the folder to write into
        if not os.path.exists(package):
            os.makedirs(package)
            # we must make sure that there is an __init__.py is every directory
            # that we have just created, otherwise Python will complain about
            # missing modules
            self.__ensure_packages(package)
        
        # calculate the path where we will write the module
        path = os.path.join(package, path[-1] + ".py")
        # ensure that we are not about to overwrite an existing module
        if os.path.exists(path):
            raise InstallError("The target (%s) already exists in the repository." % module)
        # write the module file into the package
        if fs.write(path, source) != None:
            return True
        else:
            raise InstallError("Failed to write module to repository.")
            
            
class InstallError(Exception):
    pass
