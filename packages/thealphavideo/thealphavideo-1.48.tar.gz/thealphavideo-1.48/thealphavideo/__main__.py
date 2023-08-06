from flask import Flask, render_template, request, url_for, flash, redirect, Response, session
from pygtail import Pygtail
from flask_ask_alphavideo import Ask, question, statement, convert_errors, audio
from youtube_dl import YoutubeDL
from werkzeug.exceptions import abort
import sqlite3
import logging
import datetime
import os
import sys
import time
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# version 1.5


def get_db_connection():
    conn = sqlite3.connect('/data/database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def start():
    sentry_sdk.init(
        dsn="https://d781c09d67f34a05b2b2d89193f4f2a0@o575799.ingest.sentry.io/5728581",
        integrations=[FlaskIntegration()],
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )


ip = '0.0.0.0'  # System Ip
host = '0.0.0.0'  # doesn't require anything else since we're using ngrok
port = 5000  # may want to check and make sure this port isn't being used by anything else

LOG_FILE = 'app.log'
log = logging.getLogger('__name__')
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

ytdl_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': False,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': ip
}

ytdl = YoutubeDL(ytdl_options)
app = Flask(__name__)
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", True)
app.config["JSON_AS_ASCII"] = False
app.config['SECRET_KEY'] = 'dev'
app.config['PUBLIC']=os.environ.get("public", "False") == "True"
app.config.from_mapping(
    BASE_URL="http://localhost:5000",
)

print("By AndrewsTech")


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def not_found_error(error):
    return render_template('405.html'), 405


if app.config["PUBLIC"]:
    import public
else:
    import pages 



ask = Ask(app, '/api')


@ask.launch
def launch():
    card_title = render_template('card_title')
    question_text = render_template('welcome')
    return question(question_text).simple_card(card_title, question_text)


@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent('AMAZON.StopIntent')
def handle_stop_intent():
    stop = render_template('stop')
    return statement(stop)


@ask.intent('AMAZON.CancelIntent')
def handle_stop_intent():
    stop = render_template('stop')
    return statement(stop)


@ask.intent('AMAZON.PauseIntent')
def handle_pause_intent():
    pause = render_template('pause')
    return audio(pause).stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    resume = render_template('resume')
    return audio(resume).resume()


@ask.intent('AMAZON.FallbackIntent')
def handle_fallback_intent():
    fallback = render_template('fallback')
    return question(fallback)


@ask.intent('AMAZON.HelpIntent')
def handle_help_intent():
    fallback = render_template('fallback')
    return question(fallback)


@ask.intent('QueryIntent', mapping={'query': 'Query'})
def handle_query_intent(query):
    if not query or 'query' in convert_errors:
        return question('no results found, try another search query')

    data = ytdl.extract_info(f"ytsearch:{query}", download=False)
    search_results = data['entries']

    if not search_results:
        noresult = render_template('noresult')
        session.attributes[search_results] = search_results
        return question(noresult)

    result = search_results[0]
    song_name = result['title']
    channel_name = result['uploader']

    for format_ in result['formats']:
        if format_['ext'] == 'm4a':
            mp3_url = format_['url']
            playing = render_template('playing', song_name=song_name, channel_name=channel_name)
            return audio(playing).play(mp3_url)

    return question('noresult')


app.run(host=host, port=port)

# Made by andrewstech https://github.com/unofficial-skills/alpha-video/
