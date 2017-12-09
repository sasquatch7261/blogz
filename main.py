from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:BeProductive@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

blogs = ["One", "Two", "Three"]

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        new_blog = Blog(title = request.form['title'], body = request.form['body'])
        db.session.add(new_blog)
        db.session.commit()

    blogs = Blog.query.all()

    return render_template("edit.html", blogs = blogs)

if __name__ == '__main__':
    app.run()