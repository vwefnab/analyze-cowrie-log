


class session:



    def __init__(self, id_in='0', protocol_in='Prot_unknown', port_dst_in=0, time_start_in='time_unknown' ):
        self.id = id_in
        self.protocol = protocol_in
        self.port_dst = port_dst_in
        self.time_start = time_start_in
        self.file_download = list()
        self.commands = list()
        self.time_end = 'time_unknown'
        self.time_duration = 'time_unknown'




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

    def info_to_string(self):
        print('protocol: ' + self.protocol)
        print('id: ' + self.id)
        print('Port: ' + str(self.port_dst))
        print('time_start: ' + self.time_start)
