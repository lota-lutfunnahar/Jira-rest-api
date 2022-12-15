import math
from typing import Mapping, Any

import requests as rest

import jira_dir


def get_all(endpoint: str, what: str, params: Mapping[str, Any] = None) -> Mapping[str, Any]:
    if params is None:
        params = {}

    url = jira_dir.API_URL + endpoint + '?jql=assignee in (621dde62a124500068869fe0) AND worklogDate >= startOfMonth("-1") AND worklogDate < startOfMonth() order by created DESC'

    data = rest.get(url, auth=jira_dir.AUTH).json()

    print('OK GET', endpoint)

    if data['total'] > data['maxResults']:
        for page in range(1, math.ceil(data['total'] / data['maxResults'])):
            temp = rest.get(url, auth=jira_dir.AUTH, params={
                # **params,
                'startAt': page * jira_dir.PAGE_SIZE  # specify the offset
            }).json()
            print('OK GET', endpoint)

    return data


def get_board(endpoint: str, what: str, params: str):
    if params is None:
        params = {}

    url = jira_dir.API_SPT_URL + endpoint + '/' + params + '/sprint'
    print(url)

    respose = rest.get(url, auth=jira_dir.AUTH).json()

    print(respose)
    print('OK GET', endpoint)

    data = []

    if respose['maxResults'] > 0:
        for i in respose['values']:
            data.append(i)
        print('OK GET data', data)

    return data