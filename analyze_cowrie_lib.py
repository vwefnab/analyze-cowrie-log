from datetime import datetime


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

    def add_sessions_list(self, session_list):
        self.sessions = session_list





class cow_command:
    def __init__(self, command_in, timestamp_in):
        self.cmd = command_in
        self.timestamp = timestamp_in

    def get_cmd(self):
        return self.cmd

    def get_time(self):
        return self.timestamp

    def get_cmd_str_strip(self):
        split = self.cmd.split(' ')
        return split

    def time_to_seconds(self):
        utc_time = datetime.strptime(self.timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        epoch = (utc_time - datetime(1970, 1, 1)).total_seconds()

        return epoch

    def info_to_string(self):
        print(self.timestamp + '\t' + self.cmd)






class cow_file:

    def __init__(self, shasum_in='not defined', url_in='http://', path_dest_in='not defined'):

        self.shasum =shasum_in
        self.url = url_in
        self.path_dest = path_dest_in

    def get_sha(self):
        return self.shasum

    def get_url(self):
        return self.url

    def get_path_dest(self):
        return self.path_dest

    def info_to_string(self):
        print('URL: ' + self.url)
        print('Path_dest: ' + self.path_dest)
        print('SHAsum: ' + self.shasum)






class session:



    def __init__(self, id_in='0', ipaddress_in='0.0.0.0', protocol_in='Prot_unknown', port_dst_in=0, time_start_in='time_unknown', password_in='', username_in='' ):
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
        self.login_success = False
        self.password = password_in
        self.username = username_in




    def get_id(self):
        return self.id
    def get_ip(self):
        return self.ipaddress

    def get_password(self):
        return self.password

    def get_username(self):
        return self.username

    def get_login_success(self):
        return self.login_success

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

    def get_commands(self):
        return self.commands

    def get_all_commands(self):
        dlist = list()
        for cmd in self.commands:
            for c in cmd.get_cmd_str_strip():
                dlist.append(c)
            dlist.append('#ENTER#')
        return dlist

    def set_login_success(self, bool):
        self.login_success = bool

    def set_password(self, passwd):
        self.password = passwd

    def set_username(self, uname):
        self.username = uname

    def set_session(self, bool=True):
        self.session_success = bool

    def set_time_end(self, time):
        self.time_end = time

    def set_time_duration(self, time):
        self.time_duration = time

    def add_file_obj(self, file):
        self.file_download.append(file)

    def add_files_list(self, files_list):
        self.file_download = files_list

    def add_command(self, cmd):
        self.commands.append(cmd)
    def add_commands_list(self, cmd_list):
        self.commands = cmd_list

    def get_mean_cmd_execute(self):
        if len(self.commands) <= 1:
            return 0
        else:
            count=0
            diff = 0
            while count < len(self.commands)-1:
                diff += self.commands[count+1].time_to_seconds() - self.commands[count].time_to_seconds()
                count+=1
            mean = diff / (len(self.commands)-1)

        return mean

    def info_to_string(self):
        print('protocol: ' + self.protocol)
        print('ipaddress: ' + self.ipaddress)
        print('id: ' + self.id)
        print('Port: ' + str(self.port_dst))
        print('time_start: ' + self.time_start)
        print('time_end ' + self.time_end)
        print('time_duration ' + str(self.time_duration) + '\n')



