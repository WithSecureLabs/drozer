import cStringIO
import os
import re
import zipfile

from mwr.common import fs
from mwr.droidhg.repoman.remotes import Remote

class ModuleInstaller(object):
    
    def __init__(self, repository):
        self.repository = repository
    
    def install(self, modules):
        """
        Installs a list of modules, either as local or remote specs, and returns
        a dictionary of status information.
        """
        
        status = { 'success': [], 'fail': {} }

        for pattern in modules:
            if pattern.find("/") >= 0 or pattern.find("\\") >= 0:
                fetch = self.__read_local_module
                _modules = [pattern]
            else:
                fetch = self.__read_remote_module
                _modules = self.search_index(pattern)
            
            for module in _modules:
                print "Processing %s..." % module,
                
                try:
                    self.__install_module(fetch, module)
                    print "Done."
                    
                    status['success'].append(module)
                except InstallError as e:
                    print "Failed."
                    
                    status['fail'][module] = str(e) 
        
        return status
    
    def search_index(self, module):
        """
        Search the combined index view from all remotes based on a search pattern
        with optional wildcards.
        """
        
        index = self.__get_combined_index()
        
        if module.find("*") >= 0:
            return filter(lambda m: re.match(".*" + module.replace("*", ".*") + ".*", m) != None, index)
        else:
            return filter(lambda m: m == module, index)
    
    def __create_package(self, package):
        """
        Create a Python package within the repository.
        """
        
        if not os.path.exists(package):
            os.makedirs(package)
            # we must make sure that there is an __init__.py is every directory
            # that we have just created, otherwise Python will complain about
            # missing modules
            self.__ensure_packages(package)
        
        return package
    
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
    
    def __get_combined_index(self):
        """
        Fetches INDEX files from all known remotes, and builds a combined INDEX
        listing of all available modules.
        """
        
        index = set([])
        
        for url in Remote.all():
            source = Remote.get(url).download("INDEX")
            
            if source != None:
                index = index.union(source.split("\n"))
        
        return filter(lambda m: m != None and m != "", index)

    def __install_module(self, fetch, module):
        """
        Install a module into a repository.
        """

        source = fetch(module)
        
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
        
        for url in Remote.all():
            source = Remote.get(url).download(module)
            
            # if we found the source, we return straight away - this allows us to
            # install the module from the first source that we come across
            if source != None:
                return source
        
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
            return self.__unpack_module_zip(module, source)
        
        return True
    
    def __unpack_module_raw(self, module, source):
        """
        Handles unpacking a module and installing it, if the source is a Python
        module.
        """
        
        path = module.split(".")
        
        # create a Python package to write the module into
        package = self.__create_package(os.path.join(self.repository, *path[0:-1]))
        
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
        
    def __unpack_module_zip(self, module, source):
        """
        Handles unpacking a module and installing it, if the source is a zipped
        archive.
        """
        
        path = module.split(".")[0:-1]
        # when extracting the path, we drop the last segment, because it'll be '.zip'
        
        # create a Python package to write the module into
        package = self.__create_package(os.path.join(self.repository, *path))
        
        # get a list of files within the archives
        archive = zipfile.ZipFile(cStringIO.StringIO(source))
        files = archive.infolist()
        # ensure we are not about to overwrite any existing files
        if True in map(lambda f: os.path.exists(os.path.join(package, f.filename)), files):
            raise InstallError("Installing this module would overwrite one-or-more files in your repository.")
        # extract each file, in turn
        try:
            for f in files:
                archive.extract(f, package)
        except IOError:
            raise InstallError("Fatal error whilst unpacking the zip archive.")
        
        return True
            
class InstallError(Exception):
    pass
