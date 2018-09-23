import os
import json
from cow_file import cow_file
from cow_client import cow_client
from session import session

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


    for f in json_list:

        try:
            file_path = f
            file_list = [line.rstrip('\n') for line in open(file_path)]
            for i in file_list:
                all_json.append(json.loads(i))

        except:
            print('Could not open file: ' + file_path)
    return all_json


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


def json_to_objects(json_data):
    #ip_addresses_list = list()
    #cow_client_list = list()
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

                print('session ' + json_line['session'] + ': ' + str(index))

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




    for c in closed_sessions:
        files = c.get_files()
        for f in files:
            f.info_to_string()






data = fuse_all_json()

json_to_objects(data)
