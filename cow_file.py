


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

