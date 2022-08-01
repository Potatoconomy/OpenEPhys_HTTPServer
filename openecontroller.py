"""
Author: Patrick Campbell
Universitaet Freiburg
"""

import requests
import sys
import json


class myClient:
    """
    Creates a HTTP communication instance with OpenEPhys Acquisition Board
    """
    def __init__(self, record_path, parent_dir):
        """
        http://localhost:37497/api/status -- Put in web address to check connection.
        May need to activate HTTP Server Connection in OEP
            :param record_path: -- name of your data file
            :param parent_dir: -- parent directory of record_path
        """
        self.host = 'http://localhost:37497'
        self.status_url = self.host + "/api/status"
        self.message_url = self.host + "/api/message"
        self.recording_url = self.host + "/api/recording"
        self.record_path = record_path
        self.parent_dir = parent_dir

    def set_acquisition_mode(self, mode):
        """
        Switch between IDLE, ACQUIRE, and RECORD
        """
        if mode not in ['IDLE', 'ACQUIRE', 'RECORD']:
            print("Improper Mode set. Exiting.")
            sys.exit(1)

        if mode == 'IDLE':
            r = requests.put(self.status_url, data=b'{"mode":"IDLE"}')
        elif mode == 'ACQUIRE':
            r = requests.put(self.status_url, data=b'{"mode":"ACQUIRE"}')
        elif mode == 'RECORD':
            r = requests.put(self.status_url, data=b'{"mode":"RECORD"}')
        return r

    def get_status(self):
        """
        Run to check status of HTTP Connection with OEP
        """
        try:
            r = requests.get(self.status_url)
        except requests.exceptions.ConnectionError:
            print("Please check OpenEPhys and Internet Connection. Exiting.") # Could change this to a try again
            sys.exit(1)
        return r

    def set_recording_options(self):
        """
        Change GUI Recording settings
        JSON String on URL:
            {"append_text":"",
            "base_text":"YYYY-MM-DD_HH-MM-SS",
            "default_record_engine":"BINARY",
            "parent_directory":"/Users/nes/Documents/Open Ephys",
            "prepend_text":"",
            "record_nodes":[{"experiment_number":1,
                             "is_synchronized":true,
                             "node_id":106,
                             "parent_directory":"/Users/nes/Documents/Open Ephys",
                             "record_engine":"BINARY",
                             "recording_number":0}]}
        """
        data_ = {"append_text": "",
                 "base_text": self.record_path,
                 "default_record_engine": "BINARY",
                 "parent_directory": self.parent_dir,
                 "prepend_text": "",
                 "record_nodes": [{"experiment_number": "1",
                                   "is_synchronized": "true",
                                   "node_id": 106,
                                   "parent_directory": self.parent_dir,
                                   "record_engine": "BINARY",
                                   "recording_number": 0}]}

        json_object = json.dumps(data_)
        print("\njson object:\n %s" % json_object)
        print("\n")

        r = requests.put(self.recording_url, data=json_object)
        print(r) # prints 200 -- valid PUT

        r = requests.get(self.recording_url)
        print("recording_URL_GET:\n %s" % r.json())
        return r

