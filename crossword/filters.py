from . import app
from flask import Markup
import mistune as md

@app.template_filter()
def markdown(text):
    return Markup(md.markdown(text,escape=True))

@app.template_filter()
def dateformat(date, format):
    if not date:
        return None
    return date.strftime(format).lstrip('0')
    
@app.template_filter()
def datetimeformat(value, format='%M:%S / %m-%s'):
    return value.strftime(format)
