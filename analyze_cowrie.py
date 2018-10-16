import os
import platform
import json
from analyze_cowrie_lib import cow_file, cow_command, session, cow_client
import sys
import linecache
import math
from collections import Counter
import re




folder_path = os.path.dirname(os.path.abspath(__file__))

#This is path to .json files. If path not included as a argument it will use "folder_path"



def help_page():
    print("""
    This is the help page.
    You have to convert cowrie .json log files to .clog files before analysing.
    
    Usage:  
        analyze_cowrie.py [OPTION]
        
    Options:
    -c      Convert json log files to .clog files
        [-c PATH_IN FILE_PATH_OUT] 
    
    Aalyzing (.clog files): 
    -a      All analysing methods on .clog files.
        [-a]
        
    -m      Main info about all clients.
        [-m]
    
    -P      Most common passwords.
        [-P | -P NUMBER]
    
    -U      Most common user names.
        [-U | -U NUMBER]
    
    -u      Unique set of commands. (Default threshold is set to 80%)
        [-u]
    
    -h      Human like set of commands (Non robot)
        [-h]
    
    -d      SHASUM of all downloaded files.
        [-d]
    
    -f      Input .clog file.
        [-f PATH_IN]
    
    -o      Output to file.
        [-o PATH_OUT]
     
    Filters
    --filer-ip              Filter by specific IP-address
        [--filter-ip=IPADDRESS]
    
    --filter-nr-sessions    Filter by minimum numbers of sessions
        [--filter-nr-sessions=NUMBER]
    
    --filter-nr-downloads   Filter by minimum numbers of downloads
        [--filter-nr-downloads=NUMBER] 
        
        
    """)


def get_options(args=sys.argv):

    ##bool list of arguments status: 0: Output to file 1: convert 2: analyze all 3: main client info
    #4: common passwords 5: common usernames 6: uniq commands 7: Human sessions 8: Downloaded files 9: input file 10: filter-ip 11: filter-sessions 12: filter-downloads
    #Make all options False
    option_list = [[0],[0],[0],[0],[0],[0],[0],[0],[0],[0],[0,''],[0,0],[0,0]]
    #If any arguments except first file path been found
    if len(args) > 1:

        #Go through all arguments
        for arg in args:
            #Get help-page
            if arg in '-h':
                help_page()
                exit()
            #If all analyzing is going to be True



            #convert mode
            elif arg in '-c':
                index = args.index('-c')+1
                try:
                    option_list[1][0] = 1
                    json_path = args[index]
                    if '.json' not in json_path:
                        option_list[1].append(json_path)
                        option_list[1].append(args[index+1])

                    else:
                        new_path = os.path.dirname(json_path)
                        option_list[1].append(new_path)
                        option_list[1].append(args[index + 1])

                except:
                    print('Not enough arguments or path don\'t exists. Specify path to .json files and output path.')
                    exit(1)

            # If all analyzing is going to be True
            elif arg in '-a':
                count = 3
                while count < 10:
                    option_list[count][0] = 1
                    count+=1
            #If main client info is going to be true
            elif arg in '-m':
                option_list[3][0] = 1
            # If password option is going to be true
            elif arg in '-P':
                option_list[4][0] = 1
                try:
                    index = args.index('-P') + 1
                    if len(args)-1 >= index and ('-' not in args[index][0]):
                        option_list[4].append(int(args[index]))
                    else:
                        option_list[4].append(25)
                except:
                    print('Could not read argument for option -P.')
                    exit(1)
            # If usernames option is going to be true
            elif arg in '-U':
                option_list[5][0] = 1
                try:
                    index = args.index('-U') + 1
                    if len(args) - 1 >= index and ('-' not in args[index][0]):
                        option_list[5].append(int(args[index]))
                    else:
                        option_list[5].append(25)
                except:
                    print('Could not read argument for option -U.')
                    exit(1)
            # If uniq commands is going to be true
            elif arg in '-u':
                option_list[6][0] = 1
            # If human session is going to be true
            elif arg in '-h':
                option_list[7][0] = 1
            # If download option is going to be true
            elif arg in '-d':
                option_list[8][0] = 1
            # If input file option is going to be true
            elif arg in '-f':
                option_list[9][0] = 1
                try:
                    index = args.index('-f') + 1
                    if len(args) - 1 >= index and ('-' not in args[index][0]):
                        option_list[9].append(args[index])
                    else:
                        raise
                except:
                    print('Could not read argument for option -f.')
                    exit(1)
            #Filter ip is set
            elif '--filter-ip=' in arg:
                option_list[10][0] = 1

                try:
                    arg_value = arg[12:]
                    if len(arg_value) != 0:
                        option_list[10][1] == arg_value
                    else:
                        raise

                except:
                    print('Could not read argument for option --filter-ip.')
                    exit(1)
            #FIlter nr of sessions is set
            elif '--filter-nr-sessions=' in arg:
                option_list[11][0] = 1
                try:
                    arg_value = arg[21:]
                    if len(arg_value) != 0:
                        option_list[11][1] = int(arg_value)
                    else:
                        raise

                except:
                    print('Could not read argument for option --filter-session.')
                    exit(1)
            #FIlter nr of downloads is set
            elif '--filter-nr-downloads=' in arg:
                option_list[12][0] = 1
                try:
                    arg_value = arg[22:]
                    if len(arg_value) != 0:
                        option_list[12][1] = int(arg_value)
                    else:
                        raise

                except:
                    print('Could not read argument for option --filter-downloads.')
                    exit(1)

            #Set ooutput to file to True
            if arg in '-o':
                try:
                    index = args.index('-o') + 1
                    option_list[0][0] = 1
                    path_out = os.path.dirname(args[index])
                    if os.path.isdir(path_out):
                        option_list[0].append(args[index])
                    else:
                        raise
                except:
                    print('Not enough arguments or path don\'t exists. Specify path and name of output file')
                    exit(1)
    else:
        print('Could not find any arguments.')
        help_page()
        exit(1)

    return option_list

def get_system_path(path):


    system = platform.system()
    if 'Windows' in system:
        #A bug in PowerShell. Remove " at the end.
        if '\"' in path[-1]:
            path = path[0:len(path)-1]
        full_path = path + '\\'
    else:
        full_path = path + '/'


    return full_path





def get_files_json(path=folder_path):

    #Add / or \ if it is a directory
    if '.json' not in path:
        full_path = get_system_path(path)

    else:

        dir_name = os.path.dirname(path)
        full_path = get_system_path(dir_name)


    arr = []
    try:
        arr_first = os.listdir(full_path)
        for f in arr_first:
            if '.json' in f:
                arr.append(full_path+f)
    except:
        print('Could not get files in the main folder')

    if len(arr) > 1:
        # Put cowrie.json last in order
        arr.append(arr.pop(arr.index(full_path+'cowrie.json')))

    return arr



def get_clients_file_names(path=folder_path):

    arr = []


    try:
        if '.clog' not in path:

            full_path = get_system_path(path)
            arr_first = os.listdir(full_path)
            for f in arr_first:

                if re.search(r'(\d).clog',f):
                    arr.append(full_path+f)
        else:

            path_dir = os.path.dirname(path)
            full_path = get_system_path(path_dir)
            file_name = os.path.basename(path)


            if len(file_name) != 0:
                file_name = file_name[0:file_name.index('.clog') - 1]
            arr_first = os.listdir(path_dir)
            for f in arr_first:

                if re.search(file_name + r'(\d).clog', f):
                    arr.append(full_path+f)

    except:
        print('Could not get .clog files')
        exit(1)

    return arr



def get_all_commands(folder=folder_path):
    json_file_list = get_files_json(folder)

    if len(json_file_list) > 1:
        # Put cowrie.json last in order
        json_file_list.append(json_file_list.pop(json_file_list.index('cowrie.json')))


    session_id = set()
    for f in json_file_list:
        with open(f) as file:
            session_id_tmp = None
            command_list = list()
            for line in file:
                json_line = json.loads(line)
                if json_line['eventid'] == 'cowrie.command.input' and 'CMD' in json_line['message'][0:4]:
                    new_cow_command = cow_file(json_line['message'][5:], json_line['timestamp'])
                    command_list.append(new_cow_command)






def get_downloaded_files(client):
    sha = set()
    ses = client.get_sessions()

    for s in ses:
        files = s.get_files()
        if len(files) > 0:
            for file in files:
                sha.add(file.get_sha())
    return sha



def id_in_active_sessions(ses, active_sessions):
    bool = False
    for s in active_sessions:
        if ses in s.get_id():
            bool = True
    return bool

def index_of_active_session(ses, active_sessions):
    index = 0
    for s in active_sessions:
        if ses in s.get_id():
            break
        index += 1

    return index

def index_of_client(client, client_list):
    index = 0
    for c in client_list:
        if client in c.get_ip():
            break
        index += 1

    return index

def ip_in_clientlist(ip, client_list):
    bool = False
    for c in client_list:
        if ip in c.get_ip():
            bool = True
    return bool



def json_to_objects3(path_in, path_out):
    county = 0

    json_file_list = get_files_json(path_in)
    cow_client_list = list()

    closed_sessions = list()
    active_sessions = list()
    file_count = 1
    path_file = path_out + '1'
    file_list = [path_file]

    # Create an emty file named sessions.txt
    file_cache = open(path_file, 'w')
    file_cache.write('')
    file_cache.close()



    for f in json_file_list:


        with open(f) as file:
            session_id_tmp = None
            command_list = list()
            for line in file:
                json_line = json.loads(line)
                ip = json_line['src_ip']
                # If new session starts
                if json_line['eventid'] == 'cowrie.session.connect':

                    # make a new session object
                    try:
                        new_session = session(id_in=json_line['session'], ipaddress_in=ip,
                                              protocol_in=json_line['protocol'], port_dst_in=int(json_line['dst_port']),
                                              time_start_in=json_line['timestamp'])
                        active_sessions.append(new_session)
                    except:
                        print('Failed to create session.')


                # If it is the end of the session
                elif json_line['eventid'] == 'cowrie.session.closed':
                    if id_in_active_sessions(json_line['session'], active_sessions):
                        index = index_of_active_session(json_line['session'], active_sessions)
                        # set session object variable session_success to True
                        active_sessions[index].set_session()
                        # Add two new variables to session object
                        active_sessions[index].set_time_end(json_line['timestamp'])
                        active_sessions[index].set_time_duration(json_line['duration'])
                        # send session to closed list
                        closed_sessions.append(active_sessions[index])
                        # remove closed session from active session list
                        del active_sessions[index]



                # Between start and end of sessions
                else:
                    # Get the session object from active sessions
                    if id_in_active_sessions(json_line['session'], active_sessions):
                        index = index_of_active_session(json_line['session'], active_sessions)

                        # If session downloading a file from internet
                        if json_line['eventid'] == 'cowrie.session.file_download' and 'http' in json_line['url']:
                            # make new cow_file object
                            file_obj = cow_file(shasum_in=json_line['shasum'], url_in=json_line['url'],
                                                path_dest_in=json_line['outfile'])
                            active_sessions[index].add_file_obj(file_obj)
                        #If it states login password and username and success to login
                        elif json_line['eventid'] == 'cowrie.login.success':
                            active_sessions[index].set_login_success(True)
                            active_sessions[index].set_password(json_line['password'])
                            active_sessions[index].set_username(json_line['username'])

                        # If it states login password and username and failed to login
                        elif json_line['eventid'] == 'cowrie.login.failed':
                            active_sessions[index].set_login_success(False)
                            active_sessions[index].set_password(json_line['password'])
                            active_sessions[index].set_username(json_line['username'])

                        # if log_line is a command
                        elif json_line['eventid'] == 'cowrie.command.input' and 'CMD' in json_line['message'][0:4]:
                            # add command to
                            new_cmd = cow_command(json_line['message'][5:], json_line['timestamp'])
                            active_sessions[index].add_command(new_cmd)


                            # add all closed sessions to object cow_client

            ip_addresses_list = list()
            for ses in closed_sessions:
                ip = ses.get_ip()
                # Check if it is a new client that not exists in any obejcts already

                #if not ip_in_clientlist(ip, cow_client_list):
                if not ip in ip_addresses_list:
                    county+=1
                    ip_addresses_list.append(ip)
                    # Create cow_client
                    new_client = cow_client(ipaddress_in=ip)
                    new_client.add_new_session(ses)
                    cow_client_list.append(new_client)

                else:
                    #Get clients index in client_list. Use ip_addresses_list because it has the same order.
                    index = ip_addresses_list.index(ip)#index_of_client(ip, cow_client_list)
                    # Add new session to existing cow_client
                    cow_client_list[index].add_new_session(ses)



            #Put Cow_client_list in a file
            size = int((os.path.getsize(path_file))/1000000)
            if size > 100:
                file_count += 1
                path_file = path_out + str(file_count)
                file_list.append(path_file)
                file = open(path_file, 'w')
                file.write('')
                file.close()


            file_cache = open(path_file, 'a')
            for c in cow_client_list:
                jdump = json.dumps(c, default=lambda x: x.__dict__)
                file_cache.write(jdump + '\n')
                county += 1
            file_cache.close()

            file_cache = None
            closed_sessions = None
            cow_client_list = None
            cow_client_list = list()
            closed_sessions = list()
    #Check wich cow_client that will appear more than once and send to file
    fuse_duplicate_clients_to_file(file_list)





def fuse_duplicate_clients_to_file(file_paths):

    for clients_file in file_paths:
        dub_list = list()
        # get all ip addresses of client_objects
        numbers_lines = 0


        file = open(clients_file, 'r')
        ip_list = list()

        for f in file:
            f_json = json.loads(f)
            ip_list.append(f_json['ipaddress'])
            numbers_lines+=1
        file.close()
        file= None


        added_list = list()
        for number in range(1,numbers_lines):
            if number not in added_list:
                added_list.append(number)
                line = linecache.getline(clients_file, number)
                dub_list.append(list())
                dub_list[-1].append(number)
                line_json = json.loads(line)
                ip_main = line_json['ipaddress']


                count = 0

                for ip in ip_list:
                    count+=1
                    #If matches add that number to the dublist.
                    if (ip_main in ip) and (count not in added_list):
                        dub_list[-1].append(count)
                        added_list.append(count)


        #fuse all cow_client dublicates and send to file
        file = open(clients_file+'.clog', 'w')
        file.write('')
        file.close()

        for dub in dub_list:
            if len(dub) != 0:
                count = 0
                while count < len(dub):
                    if count == 0:
                        line = linecache.getline(clients_file, dub[count])
                        client_new = make_client_from_text(line)

                    elif count > 0:
                        line = linecache.getline(clients_file, dub[count])
                        client_tmp = make_client_from_text(line)
                        sessions = client_tmp.get_sessions()
                        for ses in sessions:
                            client_new.add_new_session(ses)
                    count+=1

                with open(clients_file+'.clog', 'a') as file:
                    jdump = json.dumps(client_new, default=lambda x: x.__dict__)
                    file.write(jdump + '\n')
                file.close()
                file = None
        linecache.clearcache()
        #delete tmp file
        os.remove(clients_file)



def export_objects_to_analyze_logs(clients_list, outfile='testtest.txt'):

    with open(outfile, 'w') as output:
        for c in clients_list:

            jdump = json.dumps(c, default=lambda x: x.__dict__)

            output.write(jdump + '\n')

        output.close()

def import_session_from_file(text):
    ses = json.loads(text)


    commands = ses['commands']
    commands2 = list()
    if len(commands) > 0:
        for c in commands:
            # new cmd object
            cmd_new = cow_command(command_in=c['cmd'], timestamp_in=c['timestamp'])
            commands2.append(cmd_new)
    downloads = ses['file_download']
    downloads2 = list()
    if len(downloads) > 0:
        for d in downloads:
            # new cow_file onject
            cow_file_new = cow_file(shasum_in=d['shasum'], url_in=d['url'], path_dest_in=d['path_dest'])
            downloads2.append(cow_file_new)
    session_new = session(id_in=ses['id'], ipaddress_in=ses['ipaddress'], protocol_in=ses['protocol'],
                          port_dst_in=ses['port_dst'], time_start_in=ses['time_start'])
    session_new.add_commands_list(commands2)
    session_new.add_files_list(downloads2)
    session_new.set_time_end(ses['time_end'])
    session_new.set_time_duration(ses['time_duration'])


    return session_new

def make_client_from_text(text):

    json_line = json.loads(text)
    ip = json_line['ipaddress']
    #make new cow_client object
    cow_client_new = cow_client(ipaddress_in=ip)
    sessions = json_line['sessions']
    session2 = list()
    for ses in sessions:
        commands = ses['commands']
        commands2 = list()
        if len(commands) > 0:
            for c in commands:
                #new cmd object
                cmd_new = cow_command(command_in=c['cmd'], timestamp_in=c['timestamp'])
                commands2.append(cmd_new)
        downloads = ses['file_download']
        downloads2 = list()
        if len(downloads) > 0:
            for d in downloads:
                #new cow_file onject
                cow_file_new = cow_file(shasum_in=d['shasum'], url_in=d['url'], path_dest_in=d['path_dest'])
                downloads2.append(cow_file_new)
        session_new = session(id_in=ses['id'], ipaddress_in=ses['ipaddress'], protocol_in=ses['protocol'], port_dst_in=ses['port_dst'], time_start_in=ses['time_start'])
        session_new.add_commands_list(commands2)
        session_new.add_files_list(downloads2)
        session_new.set_time_end(ses['time_end'])
        session_new.set_time_duration(ses['time_duration'])
        session_new.set_password(ses['password'])
        session_new.set_username(ses['username'])
        session_new.set_login_success(ses['login_success'])
        session2.append(session_new)
    #add more to cow_client object
    cow_client_new.add_sessions_list(session2)
    #add cow_client onj to list


    return cow_client_new




def import_from_analyze_logs(file):
    cow_client_list = list()

    with open(file) as ff:
        for f in ff:
            json_line = json.loads(f)
            ip = json_line['ipaddress']
            #make new cow_client object
            cow_client_new = cow_client(ipaddress_in=ip)
            sessions = json_line['sessions']
            session2 = list()
            for ses in sessions:
                commands = ses['commands']
                commands2 = list()
                if len(commands) > 0:
                    for c in commands:
                        #new cmd object
                        cmd_new = cow_command(command_in=c['cmd'], timestamp_in=c['timestamp'])
                        commands2.append(cmd_new)
                downloads = ses['file_download']
                downloads2 = list()
                if len(downloads) > 0:
                    for d in downloads:
                        #new cow_file onject
                        cow_file_new = cow_file(shasum_in=d['shasum'], url_in=d['url'], path_dest_in=d['path_dest'])
                        downloads2.append(cow_file_new)
                session_new = session(id_in=ses['id'], ipaddress_in=ses['ipaddress'], protocol_in=ses['protocol'], port_dst_in=ses['port_dst'], time_start_in=ses['time_start'])
                session_new.add_commands_list(commands2)
                session_new.add_files_list(downloads2)
                session_new.set_time_end(ses['time_end'])
                session_new.set_time_duration(ses['time_duration'])
                session2.append(session_new)
            #add more to cow_client object
            cow_client_new.add_sessions_list(session2)
            #add cow_client onj to list
            cow_client_list.append(cow_client_new)


    return cow_client_list





def get_main_client_info(client, nr_sessions=0, ipaddress='', nr_downloads=0):
    list_print = list()
    ip = client.get_ip()
    sessions = client.get_sessions()
    nr_ses = len(sessions)
    nr_download = 0
    passwords = list()
    uniq_files = list()
    nr_uniq_files = 0


    for ses in sessions:
        if ses != None:
            #Get passwords
            if not ses.get_password() in passwords:
                passwords.append(ses.get_password())
            files = ses.get_files()
            if nr_download != None:
                nr_download += len(files)
            for down in files:
                sha = down.get_sha()
                if not sha in uniq_files:
                    uniq_files.append(sha)
            if nr_uniq_files != None:
                nr_uniq_files = len(uniq_files)

    if nr_ses >= nr_sessions and ipaddress in ip and nr_download >= nr_downloads:
        list_print.append(ip)
        list_print.append('SESSIONS: '+ str(nr_ses))
        list_print.append('DOWNLOADS: '+str(nr_download))
        list_print.append('UNIQ_FILES: '+ str(nr_uniq_files))
        list_print.append('UNIQ_PASSWD: '+ str(len(passwords)))
    return list_print




def print_info_test(clients):
    for c in clients:
        print('\nClient: ' + c.get_ip() + '\tNumber of sessions: ' + str(c.get_session_count()))
        sessions = c.get_sessions()
        for s in sessions:
            print('\tSession: ' + s.get_id() + '\tDuration: ' + str(s.get_time_duration()) + ' seconds\n')

            commands = s.get_commands()
            if len(commands) > 0:
                print('\t\tCommands:\n')
                for cmd in commands:
                    print('\t\t' + cmd.get_time() + '\t' + cmd.get_cmd())
            else:
                print('\t\tNo commands')


def get_all_commands(client):
    sessions = client.get_sessions()
    command_list = list()

    for ses in sessions:

        commands = ses.get_all_commands()
        if len(commands) != 0:
            command_list.append(commands)
    return command_list


def check_if_robot(client):
    sessions = client.get_sessions()


    for ses in sessions:

        mean = ses.get_mean_cmd_execute()
        if mean < 10.0:
            return True
        else:
            return False

def get_passwords_from_client(client):
    sessions = client.get_sessions()
    passwords = list()
    for ses in sessions:
        passwd = ses.get_password()
        passwords.append(passwd)
    return passwords

def get_usernames_from_client(client):
    sessions = client.get_sessions()
    usernames = list()
    for ses in sessions:
        user = ses.get_username()
        usernames.append(user)
    return usernames

##bool list of arguments status: 0: Output to file 1: convert 2: analyze all 3: main client info
#4: common passwords 5: common usernames 6: uniq commands 7: Human sessions 8: Downloaded files 9: input file 10: filter-ip 11: filter-sessions 12: filter-downloads
#See how many uniq set och commands a client have executed.
def compare_clients(path_in, path_out='',bool_main_info=0, bool_passwords=0, bool_usernames=0, bool_uniq_cmds=0,
                    bool_check_if_robot=0,bool_downloaded_files=0, bool_filter_ip=0, filter_ip='', bool_filter_ses=0, filter_ses=0,
                    bool_filter_downloads=0,filter_downloads=0, thr_uniq_cmd=80,nr_common_pass=25, nr_common_users=25):

    client_files_list = get_clients_file_names(path_in)
    new_command_list = list()
    all_passwords = list()
    all_usernames = list()
    if_robot_out = ''
    all_downloads = set()
    all_main_info = list()

    #check if any filter is beeing used

    filter_sum = bool_filter_ip + bool_filter_ses + bool_filter_downloads

    if filter_sum > 0:
        bool_filter = True
    else:
        bool_filter = False


    for client_file in client_files_list:

        with open(client_file) as file:

            for line in file:
                client = make_client_from_text(line)
                client_sum = 0
                #Filter clients
                if bool_filter:

                    if bool_filter_ip and client_sum == 0:
                        if client.get_ip() not in filter_ip:
                            client_sum += 1
                    if bool_filter_ses and client_sum == 0:
                        if len(client.get_sessions()) < filter_ses:
                            client_sum += 1
                    if bool_filter_downloads and client_sum == 0:
                        sessions = client.get_sessions()
                        downloads_sum = 0
                        for s in sessions:
                            downloads_sum += len(s.get_files())
                        if downloads_sum < filter_downloads:
                            client_sum += 1

                if client_sum == 0:

                    # Get main info
                    if bool_main_info:
                        all_main_info.append(get_main_client_info(client))

                    # Get most common passwords
                    if bool_passwords:
                        passwords = get_passwords_from_client(client)
                        for p in passwords:
                            all_passwords.append(p)

                    # Get most common usernames
                    if bool_passwords:
                        usernames = get_usernames_from_client(client)
                        for u in usernames:
                            all_usernames.append(u)

                    # Get commands from sessions that dont act as robot
                    if bool_check_if_robot:
                        if not check_if_robot(client):
                            if_robot_out += '\n---------NOT A ROBOT---------\n'
                            if_robot_out += 'Client: ' + client.get_ip() + '\n-----------------------------\n'
                            sessions = client.get_sessions()
                            for ses in sessions:
                                commandos = ses.get_commands()
                                if len(commandos) > 1:
                                    for com in commandos:
                                        if_robot_out += com.get_time() + ' ' + com.get_cmd() + '\n'

                    # Get all uniq commands
                    if bool_uniq_cmds:
                        command_list = get_all_commands(client)
                        if len(command_list) != 0:
                            for clist in compare_commands(command_list, threshold=thr_uniq_cmd):
                                new_command_list.append(clist)

                    # Get downloaded files<<
                    if bool_downloaded_files:
                        client_downloads = get_downloaded_files(client)
                        for sha in client_downloads:
                            all_downloads.add(sha)



        #Run all the individual uniq commands against the others
    if bool_uniq_cmds:
        if len(new_command_list) > 1:
            new_command_list = compare_commands(new_command_list, threshold=thr_uniq_cmd)
        #Delete #ENTER# from all command sets
        new_command_list2 = delete_enter_str(new_command_list)


    #Print output-----------
    #-----------------------

    #Check and change if stdout should be to console or to file.
    if len(path_out) > 0:
        sys.stdout = open(path_out, 'w')

    if bool_main_info:
        all_main_info.sort(key=sort_key_session, reverse=True)
        for client_info in all_main_info:
            info_string = ''
            for info in client_info:
                info_string += info + '\t\t'
            print(info_string)


    if bool_check_if_robot:
        print('\n\n\n\n\n\n\n\n--------------\nCHECK IF ROBOT\n--------------\n\n')
        print(if_robot_out)

    if bool_uniq_cmds:
        print('\n\n\n\n\n\n\n\n-----------------------------\nGET ALL UNIQUE SET OF COMMANDS\n-----------------------------\n\n')
        count = 0
        for cmd_list in new_command_list2:
            count+=1
            print('UNIQUE: ' + str(count) + '\n')
            for cmd in cmd_list:
                print(cmd)
            print('\n--------------------------------\n')

    # Get all passwords
    if bool_passwords:
        print('\n\n\n\n\n\n\n\n-------------------------\nGET MOST COMMON PASSWORDS\n-------------------------\n\n')
        pass_count = Counter(all_passwords)
        for pas in pass_count.most_common(nr_common_pass):
            print(pas)

    # Get all usernames
    if bool_passwords:
        print('\n\n\n\n\n\n\n\n-------------------------\nGET MOST COMMON USERNAMES\n-------------------------\n\n')
        user_count = Counter(all_usernames)
        for user in user_count.most_common(nr_common_users):
            print(user)

    # Get all usernames
    if bool_downloaded_files:
        print('\n\n\n\n\n\n\n\n-------------------------\nGET ALL DOWNLOADED FILES\n-------------------------\n\n')
        for sha in all_downloads:
            print(sha)




def sort_key_session(element):
    text_session = element[1]
    size = int(text_session[10:])
    return size

def delete_enter_str(new_command_list):
    new_command_list2 = list()
    for cmd_list in new_command_list:
        count = 0
        index_list = list()
        temp_command_list = list()
        text_string = ''
        while count < len(cmd_list):
            if '#ENTER#' in cmd_list[count]:
                temp_command_list.append(text_string)
                text_string = ''
            else:
                text_string += ' ' + str(cmd_list[count])
            count += 1
        new_command_list2.append(temp_command_list)

    return new_command_list2

def compare_commands(cmd_list, threshold=80):
    add_index_list = list()
    temp_uniq_list = list()
    uniq_list = list()
    new_list = list()
    uniq_counts = 1
    orginal_list = cmd_list
    while uniq_counts != 0:
        count = 0
        uniq_counts = 0
        uniq_list.append(cmd_list[0])
        while count<len(cmd_list):
            #cos = get_cosine(Counter(cmd_list[0]), Counter(cmd_list[count]))
            compare_strings = equal_strings(cmd_list[0], cmd_list[count])
            if int(compare_strings*100) <= threshold:
                add_index_list.append(count)
                temp_uniq_list.append(cmd_list[count])
                uniq_counts+=1
                #print('Cosine:', cos, '\nEquals:', compare_strings, ' ==== ', cmd_list[0], 'XXXXXXXXXXXXXXX', cmd_list[count])
            count+=1

        cmd_list = temp_uniq_list
        temp_uniq_list = list()


    return uniq_list




def get_cosine(v1, v2):

    intersection = set(v1.keys()) & set(v2.keys())
    numerator = sum([v1[x] * v2[x] for x in intersection])

    sum1 = sum([v1[x]**2 for x in v1.keys()])
    sum2 = sum([v2[x]**2 for x in v2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    result = 0.0
    if denominator:
       result = float(numerator / denominator)

    return result


def equal_strings(list1, list2):
    count1 = 0
    count2 = 0
    for cmd in list1:
        if cmd in list2:
            count1+=1

    for cmd in list2:
        if cmd in list1:
            count2+=1
    result = (count1 + count2) / (len(list1) + len(list2))

    return result




def start():
   options = get_options()


   #if output file is specifyed
   if options[0][0]:
       path_output = options[0][1]
   else:
       path_output = ''

   #If convert is True
   if options[1][0] == 1:
       path_input = options[1][1]
       path_output = options[1][2]
       try:
           json_to_objects3(path_input, path_output)
       except:
           print('Failed to convert json files to .clog files.')
    #If analyzing is true
   else:
       path_input = options[9][1]
       #compare_clients(path_in=path_input, path_out=path_output, options_in=options)
       compare_clients(path_in=path_input, path_out=path_output, bool_main_info=options[3][0], bool_passwords=options[4][0],bool_usernames=options[5][0], bool_uniq_cmds=options[6][0], bool_check_if_robot=options[7][0],
                       bool_downloaded_files=options[8][0],
                       bool_filter_ip=options[10][0],filter_ip=options[10][1],
                       bool_filter_ses=options[11][0], filter_ses=options[11][1],
                       bool_filter_downloads=options[12][0], filter_downloads=options[12][1],
                       thr_uniq_cmd=80, nr_common_pass=25,
                       nr_common_users=25)


##bool list of arguments status: 0: Output to file 1: convert 2: analyze all 3: main client info
#4: common passwords 5: common usernames 6: uniq commands 7: Human sessions 8: Downloaded files 9: input file 10: filter-ip 11: filter-sessions 12: filter-downloads
#See how many uniq set och commands a client have executed.

start()




#compare_clients(80)


#json_to_objects3()
#get_all_client_info(ipaddress='192.168.1.112')
#alist =
#dlist = ['cow_clients1','cow_clients2','cow_clients3','cow_clients4']
#fuse_duplicate_clients_to_file(dlist)










