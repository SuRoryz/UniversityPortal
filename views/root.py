from main import app

from encryption import auth_middleware
from flask import redirect

@app.route('/')
@auth_middleware()
def main():
    return redirect('index')