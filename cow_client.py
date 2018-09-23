


class cow_client:

    def __init__(self, ipaddress_in='0.0.0.0'):
        self.hostname = 'hostname_unknown'
        self.ipaddress = ipaddress_in
        self.sessions = list()

    def get_ip(self):
        return self.ipaddress

    def get_sessions(self):
        return self.sessions

    def get_session_count(self):
        count = len(self.sessions)
        return count

    def add_new_session(self, ses):
        self.sessions.append(ses)

