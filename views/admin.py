
from main import app
from encryption import auth_middleware

from flask import request, Response, render_template

@app.route('/admin')
@auth_middleware()
def admin():
    return Response(response=render_template('admin.html'), status=200)