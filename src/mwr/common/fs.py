
def read(path):
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
    open(path, 'w').close()
    
def write(path, data):
    try:
        f = open(path, 'wb')
        f.write(data)
        f.close()
        
        return len(data)
    except IOError:
        return None
        