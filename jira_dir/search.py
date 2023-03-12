from typing import List, Any

import app
import jira_dir.util
import util


def get_issues(accountid:str) -> List[Any]:
    search_params = {
        'jql': f'assignee in ({accountid}) AND worklogDate >= startOfMonth("{app.MONTHS_BACKWARD_OFFSET}") AND '
               'worklogDate < startOfMonth()'
    }

    print(search_params)

    data = jira_dir.util.get_all('/search', 'issues', search_params)


    issues = [{
        'key': i['key'],
        'summary': i['fields']['summary'],
        'resolution': util.get_field(i, 'fields', 'resolution', 'name'),
        'status': util.get_field(i, 'fields', 'status', 'name')
    } for i in data['issues']]

    return issues

def get_issues_date_wise(accountid:str, start_date:str, end_date:str) -> List[Any]:
    search_params = {
        'jql': f'assignee in ({accountid}) AND worklogDate >= "{start_date}" AND worklogDate <= "{end_date}"'
    }

    print(search_params)

    data = jira_dir.util.get_all('/search', 'issues', search_params)


    issues = [{
        'key': i['key'],
        'summary': i['fields']['summary'],
        'resolution': util.get_field(i, 'fields', 'resolution', 'name'),
        'status': util.get_field(i, 'fields', 'status', 'name')
    } for i in data['issues']]

    return issues
