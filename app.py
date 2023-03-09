import dateutil
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
import time

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.template_filter('strftime')
def _jinja2_filter_datetime(values):
    convert = time.strftime("%H:%M:%S", time.gmtime(values))
    return convert

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
    else:
        jira = authenticate_via_jira(jira_dir.USER, jira_dir.PASS)
        data = print_jira_projects_out(jira)
        return render_template('dashboard.html', data=data)


@app.route('/login', methods=['POST', 'GET'])
def login():
    jira = authenticate_via_jira(request.form['username'], request.form['password'])
    if jira is None:
        flash("Authentication failed")
    else:
        session['logged_in'] = True
        data = print_jira_projects_out(jira)
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
        # if v.__getattribute__('key') == "AIML":
        #     v.__setattr__('boardid', '33')
        if v.__getattribute__('key') == "DLAQ":
            v.__setattr__('boardid', '19')
        elif v.__getattribute__('key') == "JAR":
            v.__setattr__('boardid', '5')
        # elif v.__getattribute__('key') == "PS":
        #     v.__setattr__('boardid', '29')
        elif v.__getattribute__('key') == "THREATIDR":
            v.__setattr__('boardid', '3')
        elif v.__getattribute__('key') == "PI":
            v.__setattr__('boardid', '8')
        elif v.__getattribute__('key') == "PT":
            v.__setattr__('boardid', '34')
        elif v.__getattribute__('key') == "ISMS":
            v.__setattr__('boardid', '30')
        else:
            v.__setattr__('boardid', None)

        if v.__getattribute__('boardid') is not None:
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
    print(sprint_issue_dta)
    return render_template('sprint_issue.html', info=sprint_sts_dta, data=sprint_issue_dta, url=jira_dir.URL)

@app.route('/pdUserWorklogReport')
def get_pdlogreport():
    return render_template('pd-teams.html')
@app.route('/seUserWorklogReport')
def get_selogreport():
    return render_template('se-teams.html')
@app.route('/pdUserWorklogDateWise')
def get_pddatewiselogreport():
    return render_template('date-range-log.html')
@app.route('/seUserWorklogDateWise')
def get_sedatewiselogreport():
    return render_template('se-date-range-log.html')

@app.route('/pdUserProfile')
def get_users():
    data = {
        'mstId': '621dde62a124500068869fe0',
        'apId': '5f84ef550756940075ec1f2d',
        'spId': '5fe02608dd5eb5010833660f',
        'twId': '61470fa2d747e80075cf019d',
        'musId': '627783aaea6ca0006972210d',
        'mamnId': '638840af9960988ef6c10279',
        'imranId': '6343e6afcba49e290970c792',
    }
    print(data)
    return render_template('pd_team_jira_user.html', userInfo=data)

@app.route('/seUserProfile')
def get_se_users():
    data = {
        'azId': '63883ea05fce844d606bb034',
        'palId': '63296f968b75455be452fcc1',
        'arfID': '6226c07e8a4bb60068f4d1e5',
        'rcId': '5fbcad8ecbead50069233962',
        'ansId': '60051061bd160e007504d330',
        'abId': '624bf73e2e101c006a916003',
        'raiId': '62822ba4ca7d7f0069ffb08e'
    }
    print(data)
    return render_template('se_team_jira_user.html', userInfo=data)

@app.route('/pipelineTeams')
def get_team():
    return render_template('team-wise-user.html')

@app.route('/worklog/<string:id>', methods=['GET'])
def get_worklog(id):
    print(f"Running for {jira_dir.HOST}, {MONTH_START.format('MMMM YYYY')}...")

    issues = jira_dir.search.get_issues(id)
    # print('issue',issues)
    jira_dir.worklog.attach_worklogs(issues)

    user_info = jira_dir.util.get_user_info('/user', 'issues', id)

    user_name = user_info['displayName']

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


    print('======================================== time', datetime.timedelta(seconds=total_time_spent_seconds))
    print('======================================== time', total_time_spent_seconds)

    print('========================================')
    print(f"Total in {MONTH_START.format('MMMM')}: {total_working_days} working days")
    return f"""<!DOCTYPE html>
        <html lang="ru">
            <head>
              <meta charset="UTF-8">
              <title>Title {user_name}</title>
            </head>
            <body>
                <p>Jira user <b>{user_name}</b> s <b>
                    {MONTH_START.format('MMMM YYYY', locale='en')}</b>
                    (Information <a href="{jira_dir.URL}">{jira_dir.URL}</a>)</p>
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