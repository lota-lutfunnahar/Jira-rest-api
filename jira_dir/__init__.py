import os

USERNAME = os.environ.get('JIRA_USERNAME')
HOST = os.environ.get('JIRA_HOST')
URL = 'https://asgardia.atlassian.net'
# API_URL = URL + '/rest/api/3'

API_URL = URL + '/rest/api/latest'
API_SPT_URL = URL + '/rest/agile/1.0'
API_SPR_STS_URL = URL + '/rest/agile/1.0/sprint/'
AUTH = ('l.nahar@pipelinesecurity.net', 'xyz')
PAGE_SIZE = 50
