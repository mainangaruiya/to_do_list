From flask import Flask, render_template, request, redirect, url_for
import time
import sched

app = Flask(__name__)
s = sched.sheduler(time.time, time.sleep)
reminder = []

@app.route('/')
def index():
    return render_template('index.html', reminders=reminders)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    time_str = request.form.get('time')

    time_struct = time.strptime(time_str,"%Y-%m-%dT%H:%M")
    reminder_time = time.mktime(time_strc)

    #reminder
     s.enterabs(reminder_time - 7200, 1, remind, (task,))
    reminders.append({'task': task, 'time': time_str})

    return redirect(url_for('index'))

def remind(task):
    print(f"Reminder: '{task}' is due in 2 hours!")

if __name__ == '__main__':
    app.run(debug=True)