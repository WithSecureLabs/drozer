import sys
import time

class ImportConflictResolver(object):
    """
    The ImportConflictResolver defines rules that can be applied to determine which
    module to keep in the event that two-or-more modules try to register the same
    name.
    """
    
    def resolve(self, existing, new):
        """
        resolve() accepts two modules, the existing module and the new module. It decides
        which to keep, and returns that module. 
        """
        
        if new.__name__ != existing.__name__ or new.__module__ != existing.__module__:
            # the klasses do not refer to the same type; we prefer standard  modules
            # over extensions and newer modules over old
            if new.__module__.startswith("drozer.modules.") and not existing.__module__.startswith("drozer.modules."):
                replace = True
            elif existing.__module__.startswith("drozer.modules.") and not new.__module__.startswith("drozer.modules."):
                replace = False
            elif time.strptime(existing.date, "%Y-%m-%d") < time.strptime(new.date, "%Y-%m-%d"):
                replace = True
            else:
                replace = False
            
            # at this point, we should have decided whether we want to replace the module
            # or not
            if replace:
                sys.stderr.write("Import Conflict: more than one definition for %s. Replacing %s with %s.\n" % (new.fqmn() , existing, new))
                
                return new
            else:
                sys.stderr.write("Import Conflict: more than one definition for %s. Keeping %s.\n" % (new.fqmn(), existing))
                
                return existing
        else:
            # both klasses refer to the same type, just have different class
            # handles for some reason: we probably loaded a .py and a .pyc
            return existing
            