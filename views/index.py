from main import app
from encryption import auth_middleware
from flask import request, Response, render_template

from models.Post import Post

@app.route('/index', methods=["GET"])
@auth_middleware()
def index():
    count = 10
    if "count" in request.args:
        count = request.args.get("count")
        
    return Response(response=render_template('index.html', news=Post.query.order_by(Post.date).limit(count)), status=200)