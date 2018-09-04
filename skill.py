import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
from umass_toolkit.dining import get_menu
from props import dc_names
from util import human_readable

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Welcome to the Alexa Skills Kit, you can say hello'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('UMenu', speech_text)


@ask.intent('EntreesIntent', types={'dc': 'slot'})
def get_entrees(dc):
    entrees = [meal for meal in get_menu(1) if meal['category-name'] == 'Entrees']
    speech_text = "Here are today's entrees for %s dining hall: " % dc_names[dc.id]
    speech_text += human_readable(', '.join([meal['dish-name'] for meal in entrees]))
    return statement(speech_text).simple_card('UMenu', speech_text)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    app.run(debug=True)