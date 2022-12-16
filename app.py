from flask import Flask, flash, redirect, render_template, request, session, abort
import logging
import datetime
import os

from jira import JIRA
import jira_dir
import jira_dir.search
import jira_dir.worklog
import jira_dir.util
import arrow

import html
# HACK: https://github.com/jazzband/prettytable/issues/40#issuecomment-846439234
html.escape = lambda *args, **kwargs: args[0]
from prettytable import PrettyTable

app = Flask(__name__)
app.secret_key = os.urandom(12)

jira_server = 'https://asgardia.atlassian.net/'

IS_PREV_MONTH = os.environ.get('IS_PREV_MONTH', default='1')
IS_PREV_MONTH = True if IS_PREV_MONTH.lower() in ['1', 'y', 'yes', 'true'] else False

MONTHS_BACKWARD_OFFSET = -1
MONTH_START = arrow.now().shift(months=MONTHS_BACKWARD_OFFSET).floor('month')\
    if IS_PREV_MONTH else arrow.now().floor('month')

log = logging.getLogger(__name__)

# with open("resources/config.yml", 'r') as ymlfile:
#     cfg = yaml.safe_load(ymlfile)
#     print(cfg)
#     print(cfg['host'])


# jira_server = cfg['protocol'].append('://')
# jira_server += cfg['port']

@app.route('/')
def home():

    if not session.get('logged_in'):
        return render_template('login.html')
    # else:
    #     return render_template('dashboard.html')
        # return "You are successful logged in!  <a href='/logout'>Logout</a>"


@app.route('/login', methods=['POST'])
def login():
    jira = authenticate_via_jira(request.form['username'], request.form['password'])
    if jira is None:
        flash("Authentication failed")
    else:
        session['logged_in'] = True
        data = print_jira_projects_out(jira)
        print(data)
        return render_template('dashboard.html', data=data)
    return home()


def authenticate_via_jira(username, password):
    log.info("Connecting to JIRA: %s" % jira_server)

    options = {'server': jira_server ,'verify': False}
    if username is not None and (password is not None or  not ""):
        try:
          jira = JIRA(basic_auth=(username, password), server=jira_server, validate=False, options=options)
        except Exception as e:
            log.error(
                "\nAuthentication to JIRA unsuccessful. "
                "Ensure the user used has sufficient access and that Username and Password were correct\n\n " % e)
            return None
    return jira


# This is just for debug purpose .
def print_jira_projects_out(jira):
    projects = jira.projects()
    dta = []

    for v in projects:
        if v.__getattribute__('key') == "AIML":
            v.__setattr__('boardid', '33')
        elif v.__getattribute__('key') == "DLAQ":
            v.__setattr__('boardid', '19')
        elif v.__getattribute__('key') == "JAR":
            v.__setattr__('boardid', '5')
        elif v.__getattribute__('key') == "PS":
            v.__setattr__('boardid', '29')
        elif v.__getattribute__('key') == "THREATIDR":
            v.__setattr__('boardid', '3')
        else:
            v.__setattr__('boardid', None)
        dta.append(v)
    return dta


@app.route('/getBoard/<string:id>', methods=['GET'])
def get_boards(id):

    data = jira_dir.util.get_board('/board', 'issues', id)

    return render_template('sprint.html', data=data)

@app.route("/sprint" , methods=['GET', 'POST'])
def get_sprint():
    select_id = request.form.get('format')

    sprint_sts_dta = jira_dir.util.get_sprint_status('/sprint', 'issues', str(select_id))
    sprint_issue_dta = jira_dir.util.get_sprint_issue('/sprint', 'issues', str(select_id))
    print('selected value', str(select_id))
    print('selected value response', sprint_sts_dta)
    # print('sprint value response', sprint_issue_dta)

    return render_template('sprint_issue.html', info=sprint_sts_dta)

@app.route('/worklog', methods=['GET'])
def get_worklog():
    print(f"Running for {jira_dir.HOST}, {MONTH_START.format('MMMM YYYY')}...")

    issues = jira_dir.search.get_issues()
    # print('issue',issues)
    jira_dir.worklog.attach_worklogs(issues)

    table = PrettyTable(['Task', 'Name', 'Status', 'Spend time'])
    data_list = []
    for issue in issues:
        if issue['timeSpentSeconds']:
            table.add_row([
                f"<a href=\"{jira_dir.URL + '/browse/' + issue['key']}\">{issue['key']}</a>",
                issue['summary'],
                issue['status'],
                datetime.timedelta(seconds=issue['timeSpentSeconds'])
            ])

    print(data_list)
    total_time_spent_seconds = 0
    for issue in issues:
        total_time_spent_seconds += issue['timeSpentSeconds']
    total_working_days = total_time_spent_seconds / 60 / 60 / 8

    print('========================================')
    print(f"Total in {MONTH_START.format('MMMM')}: {total_working_days} working days")
    return f"""<!DOCTYPE html>
        <html lang="ru">
            <head>
              <meta charset="UTF-8">
              <title>Отчёт {jira_dir.USERNAME}</title>
            </head>
            <body>
                <p>Jira user <b>{jira_dir.USERNAME}</b> s <b>
                    {MONTH_START.format('MMMM YYYY', locale='en')}</b>
                    (Information <a href="{jira_dir.URL}">{jira_dir.HOST}</a>)</p>
                {table.get_html_string(format=True)}
                <p><b>Total:</b> {total_working_days} working days
                    ({datetime.timedelta(seconds=total_time_spent_seconds)} actual time).</p>
                <p><b>Ready report:</b> {arrow.now().format(locale='en')}</p>
            </body>
        </html>"""

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.debug = True

    app.run(host='localhost', port=4000)