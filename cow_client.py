


class cow_client:

    def __init__(self, ipaddress_in='0.0.0.0'):
        self.hostname = 'hostname_unknown'
        self.ipaddress = ipaddress_in
        self.session_count = 0
        self.sessions = list()

    def get_ipaddress(self):
        return self.ipaddress

    def append_new_session(self, session_in):
        new_session = self.sessions.append(session_in)
