import traceback, sys, re, csv
from send import sendNewsletter
from flask import Flask, render_template, request
from celery import Celery
from celery.schedules import crontab
app = Flask(__name__)
app.config['DEBUG'] = True
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    CELERYBEAT_SCHEDULE={ 'monday-morning': { 'task': 'tasks.weekly', 'schedule': crontab(hour=7, minute=30, day_of_week=1), }, }
)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@celery.task()
def weekly():
   sendNewsletter()


@app.route('/')
def root():
   return render_template('index.html')

@app.route('/subscribe/', methods=['GET', 'POST'])
def subscribe():
   address = request.form['address']
   email = request.form['email']
   e_wf  = re.match(r'[^@]+@[^@]+\.[^@]+',email)
   a_wf = (address != '')
   if e_wf and a_wf:
      with open('subscribers.csv', 'a+') as f:
	reader = csv.reader(f)
        flag = True
        for row in reader:
           flag = flag and (row[0] != email)
        if flag:
           f.write(email + ',' + address + "\n")
      if flag:
         return render_template('index.html', msg = 'Successfully signed up!')
      else:
         return render_template('index.html', msg = 'Email already signed up.')
   else:
      return render_template('index.html', msg = 'Please enter a valid email and address.')

@app.route('/unsubscribe/', methods=['GET'])
def unsubscribe():
   email = request.args.get('email')
   with open('subscribers.csv', 'r') as f:
      reader = csv.reader(f)
      rows = []
      for row in reader:
         if row[0] != email:
            rows.append(row)
   with open('subscribers.csv', 'w') as f:
      writer = csv.writer(f)
      for r in rows:
         writer.writerow(r)
   return "Unsubscribed successfully!"
if __name__ == '__main__':
   app.run()
