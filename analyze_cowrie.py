import os
import json
from cow_file import cow_file
from cow_client import cow_client
from cow_command import cow_command
from session import session
import time
from sys import getsizeof

from pathlib import Path


folder_path = os.path.dirname(os.path.abspath(__file__))

#This is path to .json files. If path not included as a argument it will use "folder_path"
#json_files_path = Path('C:\\')




def get_files_json(path=folder_path):

    arr = []
    try:
        arr_first = os.listdir(path)
        for f in arr_first:
            if '.json' in f:
                arr.append(f)
    except:
        print('Could not get files in the main folder')

    return arr


def fuse_all_json():
    all_json = []

    json_list = get_files_json(folder_path)

    if len(json_list) > 1:
        # Put cowrie.json last in order
        json_list.append(json_list.pop(json_list.index('cowrie.json')))

    count = 0
    for f in json_list:

        try:

            file_path = f
            file_list = [line.rstrip('\n') for line in open(file_path)]
            for i in file_list:
                all_json.append(json.loads(i))


            count+=1
            percent = (count/len(json_list))*100
            print(str(int(percent)) + '% done')

        except:
            print('Could not open file: ' + file_path)
    return all_json


def fuse_all_json2():
    all_json = list()
    clients_list = list()

    json_list = get_files_json(folder_path)

    if len(json_list) > 1:
        # Put cowrie.json last in order
        json_list.append(json_list.pop(json_list.index('cowrie.json')))

    count = 0
    for f in json_list:

        try:
            #if not count == 0:
             #   clients_list = import_from_analyze_logs('testtest.txt')

            all_json = list()
            file_path = f
            #file_list = [line.rstrip('\n') for line in open(file_path)]
            with open(file_path) as file:
                for i in file:
                    all_json.append(json.loads(i))
            #Convert json objects to new sorted objects

            clients_list = json_to_objects(all_json, cow_client_list=clients_list)


            #export obejct to jsonfile
            #export_objects_to_analyze_logs(cow_client_temp_list)

            #remove varaiables from memmory

            file_list = None
            all_json = None
            #clients_list = None

            count+=1
            percent = (count/len(json_list))*100
            print(str(int(percent)) + '% ' + f)

        except:
            print('Could not open file: ' + file_path)


    return clients_list




def fuse_all_json3():
    all_json = list()
    clients_list = list()

    json_list = get_files_json(folder_path)

    if len(json_list) > 1:
        # Put cowrie.json last in order
        json_list.append(json_list.pop(json_list.index('cowrie.json')))

    count = 0
    for f in json_list:

        try:
            if not count == 0:
                clients_list = import_from_analyze_logs('testtest.txt')

            all_json = list()
            file_path = f

            with open(file_path) as file:
                for i in file:
                    all_json.append(json.loads(i))
            #Convert json objects to new sorted objects

            clients_list_tmp = json_to_objects(all_json, cow_client_list=clients_list)


            #export obejct to jsonfile
            export_objects_to_analyze_logs(clients_list_tmp)

            #remove varaiables from memmory

            file_list = None
            all_json = None
            clients_list = None

            count+=1
            percent = (count/len(json_list))*100
            print(str(int(percent)) + '% ' + f)

        except:
            print('Could not open file: ' + file_path)


    return clients_list



def get_all_commands():
    json_file_list = get_files_json(folder_path)

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


    time.sleep(5)
    print(len(command_list))





def get_downloaded_files(json_data):
    sha = set()
    for a in json_data:
        if a['eventid'] == 'cowrie.session.file_download' and 'http' in a['url']:
            sha.add(a['shasum'])
    for s in sha:
        print(s)


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

def json_to_objects2():
    county = 0
    json_file_list = get_files_json(folder_path)
    cow_client_list = list()
    closed_sessions = list()
    active_sessions = list()
    ip_addresses_list = list()

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

                        # if log_line is a command
                        elif json_line['eventid'] == 'cowrie.command.input' and 'CMD' in json_line['message'][0:4]:
                            # add command to
                            new_cmd = cow_command(json_line['message'][5:], json_line['timestamp'])
                            active_sessions[index].add_command(new_cmd)


                            # add all closed sessions to object cow_client


            for ses in closed_sessions:
                ip = ses.get_ip()
                # Check if it is a new client that not exists in any obejcts already

                #if not ip_in_clientlist(ip, cow_client_list):
                if not ip in ip_addresses_list:
                    county+=1
                    ip_addresses_list.append(ip)
                    # Creat cow_client
                    new_client = cow_client(ipaddress_in=ip)
                    new_client.add_new_session(ses)
                    cow_client_list.append(new_client)

                else:
                    #Get clients index in client_list. Use ip_addresses_list because it has the same order.
                    index = ip_addresses_list.index(ip)#index_of_client(ip, cow_client_list)
                    # Add new session to existing cow_client
                    cow_client_list[index].add_new_session(ses)


    print(county)
    return cow_client_list






def json_to_objects(json_data, cow_client_list=list()):

    active_sessions = list()
    closed_sessions = list()

    for json_line in json_data:
        ip = json_line['src_ip']
        #If new session starts
        if json_line['eventid'] == 'cowrie.session.connect':

            #make a new session object
            try:
                new_session = session(id_in=json_line['session'], ipaddress_in=ip, protocol_in=json_line['protocol'], port_dst_in=int(json_line['dst_port']), time_start_in=json_line['timestamp'])
                active_sessions.append(new_session)

            except:
                print('Failed to create session.')

        #If it is the end of the session
        elif json_line['eventid'] == 'cowrie.session.closed':
            if id_in_active_sessions(json_line['session'], active_sessions):
                index = index_of_active_session(json_line['session'], active_sessions)
                #set session object variable session_success to True
                active_sessions[index].set_session()
                #Add two new variables to session object
                active_sessions[index].set_time_end(json_line['timestamp'])
                active_sessions[index].set_time_duration(json_line['duration'])
                #send session to closed list
                closed_sessions.append(active_sessions[index])
                #remove closed session from active session list
                del active_sessions[index]



        #Between start and end of sessions
        else:
            #Get the session object from active sessions
            if id_in_active_sessions(json_line['session'], active_sessions):
                index = index_of_active_session(json_line['session'], active_sessions)

                #If session downloading a file from internet
                if json_line['eventid'] == 'cowrie.session.file_download' and 'http' in json_line['url']:
                    #make new cow_file object
                    file_obj = cow_file(shasum_in=json_line['shasum'], url_in=json_line['url'], path_dest_in=json_line['outfile'])
                    active_sessions[index].add_file_obj(file_obj)

                #if log_line is a command
                elif json_line['eventid'] == 'cowrie.command.input' and 'CMD' in json_line['message'][0:4]:
                    #add command to
                    new_cmd = cow_command(json_line['message'][5:], json_line['timestamp'])
                    active_sessions[index].add_command(new_cmd)


    #add all closed sessions to object cow_client
    ip_addresses_list = list()


    for ses in closed_sessions:
        ip = ses.get_ip()
        #Check if it is a new client that not exists in any obejcts already
        if not ip_in_clientlist(ip, cow_client_list):
            ip_addresses_list.append(ip)
            #Creat cow_client
            new_client = cow_client(ipaddress_in=ip)
            new_client.add_new_session(ses)
            cow_client_list.append(new_client)

        else:
            if ip_in_clientlist(ip, cow_client_list):
                index = index_of_client(ip, cow_client_list)
                # Add new session to existing cow_client
                cow_client_list[index].add_new_session(ses)

    active_sessions = None
    closed_sessions = None
    json_data = None
    return cow_client_list



def export_objects_to_analyze_logs(clients_list):

    with open('testtest.txt', 'w') as output:
        for c in clients_list:

            jdump = json.dumps(c, default=lambda x: x.__dict__)

            output.write(jdump + '\n')



        output.close()



def import_from_analyze_logs(file):
    cow_client_list = list()

    #from_file = [line.rstrip('\n') for line in open(file)]
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




list = json_to_objects2()
size = getsizeof(list)
print(size/1000000)
time.sleep(5)
list = None
time.sleep(10)
size = getsizeof(list)
print(size/1000000)
#get_all_commands()
#clients_list = fuse_all_json2()
#print('done. now sleeping in 10 sec')
#time.sleep(10)

#print_info_test(clients_list)


