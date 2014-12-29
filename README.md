<h1>Marlon.io</h1>

A service which sends weekly updates on major Chicago crime reports in your area.

Uses <a href="http://redis.io">Redis</a>, <a href="http://celeryproject.org">Celery</a>, <a href="http://flask.pocoo.org">Flask</a>, <a href="http://plenar.io">Plenar.io</a>, and <a href="http://mailjet.com">Mailjet</a>.

To run, start redis:
<pre>$ redis-server</pre>

Initiate a celery task:
<pre>$ celery -A main.celery worker</pre>

And then run:
<pre>python main.py</pre>

This will send an email every week. 

<h2>Demo</h2>

If you don't want to wait a week, with the Flask server running (it will run without Celery and Redis, but won't do anything except serve web pages), use the form to add your email to the subscriber list. Then run:

<pre>$ python -c 'from send import sendNewsletter; sendNewsletter()'</pre>

Finally, as a non-operational feature right now, the sendNewsletter() feature will create a local file called osm.html which maps the crimes using <a href="http://folium.readthedocs.org/">Folium</a>. which plots all the relevant crimes with tooltips about their descriptions. Obviously for this to be a user feature, these HTML files would need to have unique names and URLs under Flask and be linked to in each email instead of being locally overwritten each time, but we didn't have time for it. This is just a sort of prototype of what the feature would have looked like.  
