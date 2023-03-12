import math
from typing import Mapping, Any

import requests as rest

import jira_dir


def get_all_worklog(endpoint: str, what: str, params: Mapping[str, Any] = None) -> Mapping[str, Any]:
    if params is None:
        params = {}

    url = jira_dir.API_URL + endpoint
    data = rest.get(url, auth=jira_dir.AUTH).json()

    if data['total'] > data['maxResults']:
        for page in range(1, math.ceil(data['total'] / data['maxResults'])):
            temp = rest.get(url, auth=jira_dir.AUTH, params={
                **params,
                'startAt': page * jira_dir.PAGE_SIZE  # specify the offset
            }).json()
            print('OK GET', endpoint)

    return data


def get_all(endpoint: str, what: str, params: Mapping[str, Any] = None) -> Mapping[str, Any]:
    if params is None:
        params = {}

    print("test arg", params.get('jql'))

    url = jira_dir.API_URL + endpoint + '?jql=' + params.get('jql')
    print('url is ', url)

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


def get_sprint_status(endpoint: str, what: str, params: str):
    if params is None:
        params = {}

    url = jira_dir.API_SPT_URL + endpoint + '/' + params
    print(url)

    response = rest.get(url, auth=jira_dir.AUTH).json()

    print(response)
    print('OK GET', endpoint)

    return response


def get_sprint_issue(endpoint: str, what: str, params: str):
    if params is None:
        params = {}

    url = jira_dir.API_SPT_URL + endpoint + '/' + params + '/issue?'
    print('URL', url)

    response = rest.get(url, auth=jira_dir.AUTH).json()

    # print(response)
    print('OK GET', endpoint)

    data = []

    if response['total'] is not None:
        for i in response['issues']:
            data.append(i)
    return data


def get_user_info(endpoint: str, what: str, params: str):
    if params is None:
        params = {}

    url = jira_dir.API_URL_2 + endpoint + '?accountId=' + params
    print('URL', url)

    response = rest.get(url, auth=jira_dir.AUTH).json()

    # print(response)
    print('OK GET', endpoint)
    return response
