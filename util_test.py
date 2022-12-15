import math
from typing import Mapping, Any

import requests as rest

import jira_dir

AUTH = ('l.nahar@pipelinesecurity.net', 'zXkdynEDK7X5YJ3IWAlND2A5')
API_URL = 'https://asgardia.atlassian.net' + '/rest/api/latest'
PAGE_SIZE = 50

def get_all(endpoint: str, what: str, params: Mapping[str, Any] = None) -> Mapping[str, Any]:

    if params is None:
        params = {}

    url = API_URL + endpoint + '?jql=assignee in (621dde62a124500068869fe0) AND worklogDate >= startOfMonth("-1") AND worklogDate < startOfMonth() order by created DESC'

    print("url is ", url)

    print("Auth ", AUTH)

    # data = []

    # data = rest.get(url, auth=jira_dir.AUTH, params=params)
    data = rest.get(url, auth=AUTH).json()
    print('response: 👉️', data)
    # print('response.status_code: 👉️', data.status_code)
    # print('response.headers: 👉️', data.headers)

    print('OK GET', endpoint)

    if data['total'] > data['maxResults']:
        for page in range(1, math.ceil(data['total'] / data['maxResults'])):
            temp = rest.get(url, auth=AUTH, params={
                **params,
                'startAt': page * PAGE_SIZE  # specify the offset
            }).json()
            print('OK GET', endpoint)
            # data[what] += temp[what]

    return data
