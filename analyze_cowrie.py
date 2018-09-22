import os
import json
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


def json_to_objects(json_data):
    ip_addresses_list = list()
    cow_client_list = list()
    for json_line in json_data:
        ip = json_line['src_ip']
        #If uniq ipaddress and fist log in new session
        if ip not in ip_addresses_list and json_line['eventid'] == 'cowrie.session.connect':
            ip_addresses_list.append(ip)
            client = cow_client(ipaddress_in=ip)
            #make a new session object
            try:
                new_session = session(id_in=json_line['session'], protocol_in=json_line['protocol'], port_dst_in=int(json_line['dst_port']), time_start_in=json_line['timestamp'])
                new_session.info_to_string()
                client.append_new_session(new_session)
                cow_client_list.append(client)
            except:
                print('Failed to create session.')







data = fuse_all_json()

json_to_objects(data)
