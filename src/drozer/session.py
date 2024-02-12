class Session:
    """
    Session encapsulates the parameters of a session, established between an
    Agent (device) and a Console.

    All sessions are persisted in the Sessions collection, which is a singleton
    instance of SessionCollection. Sessions are accessed by identifier.
    """
    
    def __init__(self, session_id, device, console):
        self.session_id = session_id
        self.device = device
        self.console = console
    

class SessionCollection(set):
    """
    SessionCollection provides a thin wrapper on top of a set to provide a DSL
    for interacting with the sessions.
    """
    
    def add_session(self, session_id, device, console):
        """
        Create a Session, and add it to the collection.
        """

        self.add(Session(session_id, device, console))
        
    def get(self, session_id):
        """
        Retrieve a Session from the collection, by identifier.
        """

        for session in self:
            if session.session_id == session_id:
                return session

        return None


Sessions = SessionCollection()
