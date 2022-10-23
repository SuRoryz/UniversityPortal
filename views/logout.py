from main import delete_auth_token
from flask import request, Response, render_template

@app.route('/logout', methods=["GET"])
def logout():
    delete_auth_token()

    r = redirect("login")
    r.delete_cookie('token')
    r.delete_cookie('ref_token')

    return r