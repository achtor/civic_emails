import csv, subprocess, re, time
from datetime import date, timedelta
from lib.MailjetApi import MailjetApi
from pygeocoder import Geocoder
from mjlogin import mjCon

def sendNewsletter():
   with open('subscribers.csv', 'r') as f:
      reader = csv.reader(f)
      for row in reader:
         address = row[1]
         results = Geocoder.geocode(address)
         (x,y) = results[0].coordinates
         (x,y) = (str(x), str(y))
         email = row[0]
         output = subprocess.check_output('Rscript crimeinput.r ' + x + ' ' + y, shell=True)
         crimes = re.findall('"([^"]*)"', output)
         body = '<h1>Chicago crime alert</h1>'
         anchor = date.today() - timedelta(9)
         body += '<h2>Week of ' + anchor.strftime("%x") + '</h2>'
         body += 'The following major crimes were recorded within one mile of your address:'
         body += '<ul>'
         for c in crimes:
            body += '<li> ' + c + '</li>'
         body += '</ul>'
         body += '<small>To unsubscribe, click <a href="http://localhost:5000/unsubscribe/?email=' + email + '">here</a>.</small>'
         print mjCon.send_email(fromm = 'peterx@uchicago.edu', to = email, subject = 'Civic newsletter for ' + time.strftime("%x"), message = body)
