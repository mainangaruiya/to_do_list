from flask import Flask, render_template, request, redirect, url_for
import time
import sched
from datetime import datetime

app = Flask(__name__)
s = sched.scheduler(time.time, time.sleep)
reminders = []

@app.route('/')
def index():
    check_overdue_tasks()#overdue task checker
    update_time_remaining()#for each task
    return render_template('index.html', reminders=reminders)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    time_str = request.form.get('time')

    time_struct = time.strptime(time_str,"%Y-%m-%dT%H:%M")
    reminder_time = time.mktime(time_struct)

    #reminder
    s.enterabs(reminder_time - 7200, 1, remind, (task,))
    reminders.append({'task': task, 'time': time_str})

    return redirect(url_for('index'))

def remind(task):
    print(f"Reminder: '{task}' is due in 2 hours!")

def check_overdue_tasks():
    now = datetime.now()
    for reminder in reminders:
        due_time = datetime.strptime(reminder['time'], "%Y-%m-%dT%H:%M")
        if now > due_time:
            reminder['overdue'] = True
        else:
            reminder['overdue'] = False

def update_time_remaining():
    now = datetime.now()
    for reminder in reminders:
        due_time = datetime.strptime(reminder['time'], "%Y-%m-%dT%H:%M")
        if now < due_time:
            time_diff = due_time - now
            reminder['time_remaining'] = time_diff.total_seconds()
        else:
            reminder['time_remaining'] = 0

if __name__ == '__main__':
    app.run(debug=True)
