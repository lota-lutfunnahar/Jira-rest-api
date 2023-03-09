from typing import List, Any

import arrow

import app
import jira_dir.util


def attach_worklogs(issues: List[Any]):
    for issue in issues:
        data = jira_dir.util.get_all_worklog(f"/issue/{issue['key']}/worklog", 'worklogs')
        worklogs = data['worklogs']

        issue['timeSpentSeconds'] = 0
        for record in worklogs:
            if arrow.get(record['started']) > app.MONTH_START:
                issue['timeSpentSeconds'] += record['timeSpentSeconds']
