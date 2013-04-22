"""
A library of fileystem functions.
"""

import md5

def read(path):
    """
    Utility method to read a file from the filesystem into a string.
    """
    
    try:
        f = open(path, 'rb')
        line = data = f.read()

        while line != "":
            line = f.read()
            
            data += line
                
        f.close()
        
        return data
    except IOError:
        return None
    
def touch(path):
    """
    Utility method to touch a file on the filesystem.
    """
    
    open(path, 'w').close()
    
def write(path, data):
    """
    Utility method to write a string into a filesystem file.
    """
    
    try:
        f = open(path, 'wb')
        f.write(data)
        f.close()
        
        return len(data)
    except IOError:
        return None
        
def md5sum(path):
    """
    Utility method to get the md5sum of a file on the filesystem
    """
    
    try:
        f = open(path, 'rb')
        line = data = f.read()

        while line != "":
            line = f.read()
            
            data += line
        
        f.close()
        
        return md5.new(data).digest().encode("hex")
    except IOError:
        return None
        
