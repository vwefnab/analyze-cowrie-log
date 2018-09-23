

class cow_command:

    def __init__(self, command_in, timestamp_in):
        self.cmd = command_in
        self.timestamp = timestamp_in


    def get_cmd(self):
        return self.cmd

    def get_time(self):
        return self.timestamp

    def info_to_string(self):
        print(self.timestamp +'\t' + self.cmd)

