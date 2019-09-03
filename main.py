# coding: utf-8

import sys, io, os
import requests
from requests.auth import HTTPBasicAuth
# from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime as dt
from datetime import timedelta
import json


class TogglDriver:

    def __init__(self, _token, _mail_address):
        self._token = _token  # api_token
        self._mail_address = _mail_address  # your mail address
        self._workspace_id = self.get_workspace_id(self._token)
        self.projects_dictionary = self.get_projects(_token, self._workspace_id)
        self._headers = {'Content-Type': 'application/json'}

    @staticmethod
    def get_workspace_id(api_token):
        # get workspace id from api/v8/workspaces
        r = requests.get('https://www.toggl.com/api/v8/workspaces',
                         auth=(api_token, 'api_token'))

        # JSON形式でデータのエクスポート
        data = r.json()
        Data = data[0]
        return Data['id']

    @staticmethod
    def get_projects(api_token, work_space_id):
        # return projects dictionary
        p_dictionary = {}
        r = requests.get('https://www.toggl.com/api/v8/workspaces/{0}/projects'.format(work_space_id),
                         auth=(api_token, 'api_token'))

        data = r.json()
        for d in data:
            p_dictionary[d["name"]] = d["id"]
        return p_dictionary

    def get_running_time_entry(self):
        # return time entry id of current entry
        r = requests.get('https://www.toggl.com/api/v8/time_entries/current',
                         auth=HTTPBasicAuth(self._token, 'api_token'))
        data = r.json()['data']
        if data is None:
            return None
        return data['id']

    def start(self, description, project):
        if project in self.projects_dictionary:
            pid = self.projects_dictionary[project]
        else:
            # TODO make new project
            print("Error")
            return

        params = {"time_entry": {"description": description, "pid": pid, "created_with": "python"}}
        r = requests.post('https://www.toggl.com/api/v8/time_entries/start',
                          auth=HTTPBasicAuth(self._token, 'api_token'),
                          headers=self._headers,
                          data=json.dumps(params))
        print('time entry start. HTTP status :', r.status_code)

    def stop(self, running_time_entry_id):
        url = 'https://www.toggl.com/api/v8/time_entries/' + str(running_time_entry_id) + '/stop'
        r = requests.put(url, auth=HTTPBasicAuth(self._token, 'api_token'), headers=self._headers)

        print('time entry stop. HTTP status :', r.status_code)
        return r


if __name__ == '__main__':
    token = ''  # TODO your token. check here → https://www.toggl.com/app/profile
    mail = ''  # TODO your mail
    toggl = TogglDriver(_token=token, _mail_address=mail)
    # stop running entry
    id = toggl.get_running_time_entry()
    if id is not None:
        toggl.stop(id)

    # start entry
    toggl.start("game", "Hobby")  # example, description and project
