import os
import json
from pathlib import Path


folder_path = os.path.dirname(os.path.abspath(__file__))

#This is path to .json files. If path not included as a argument it will use "folder_path"
#json_files_path = Path('')


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
    #Put cowrie.json last in order
    if len(json_list) > 1:
        json_list.append(json_list.pop(json_list.index('cowrie.json')))


    for f in json_list:

        try:
            file_path = folder_path +'\\'+ f
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



data = fuse_all_json()

get_downloaded_files(data)
