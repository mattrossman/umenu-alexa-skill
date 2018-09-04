from props import dish_expansions
import re


def human_readable(message):
    for abbr, expansion in dish_expansions.items():
        message = re.sub(r'\b%s\b' % abbr, expansion, message)
    message = message.replace('w/', 'with ')
    return message
