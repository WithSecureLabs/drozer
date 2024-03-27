
class ConnectionError(RuntimeError):
    
    def __init__(self, cause):

        # yaytagyay
        # need to figure out how to gracefully exit when there's no server to connect to
        print(RuntimeError)
        print("yayerroryay you probably didn't specify a valid drozer server and that's why you're seeing this error message")
        self.cause = cause
        