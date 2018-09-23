


class session:



    def __init__(self, id_in='0', ipaddress_in='0.0.0.0', protocol_in='Prot_unknown', port_dst_in=0, time_start_in='time_unknown' ):
        self.id = id_in
        self.ipaddress = ipaddress_in
        self.protocol = protocol_in
        self.port_dst = port_dst_in
        self.time_start = time_start_in
        self.file_download = list()
        self.commands = list()
        self.time_end = 'time_unknown'
        self.time_duration = 'time_unknown'
        self.session_success = False



    def get_id(self):
        return self.id

    def get_protocol(self):
        return self.protocol

    def get_port_dst(self):
        return self.port_dst

    def get_time_start(self):
        return self.time_start

    def get_time_end(self):
        return self.time_end

    def get_time_duration(self):
        return self.time_duration

    def get_file_download(self):
        return self.file_download

    def get_files(self):
        return self.file_download

    def set_session(self, bool=True):
        self.session_success = bool

    def set_time_end(self, time):
        self.time_end = time

    def set_time_duration(self, time):
        self.time_duration = time

    def add_file_obj(self, file):
        self.file_download.append(file)

    def info_to_string(self):
        print('protocol: ' + self.protocol)
        print('ipaddress: ' + self.ipaddress)
        print('id: ' + self.id)
        print('Port: ' + str(self.port_dst))
        print('time_start: ' + self.time_start)
        print('time_end ' + self.time_end)
        print('time_duration ' + str(self.time_duration) + '\n')



