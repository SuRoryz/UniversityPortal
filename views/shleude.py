from main import app
from encryption import auth_middleware

from flask import request, Response, render_template

from xls_parser import Parser

@app.route('/shleude')
@auth_middleware()
def shleude():
    shleude = Parser.parse_xls("rasp.xls")

    return Response(response=render_template('shleude.html', groups=list(shleude.keys())), status=200)
