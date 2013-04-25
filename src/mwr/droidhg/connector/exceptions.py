
class ConnectionError(RuntimeError):
    
    def __init__(self, cause):
        self.cause = cause
        