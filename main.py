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

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    title_error = ""
    body_error = ""

    if request.method == 'POST':
        if len(request.form['title']) < 1 or len(request.form['body']) < 1:
            if len(request.form['title']) < 1:
                title_error = "Please fill in the title"
            else:
                title_error = ""

            if len(request.form['body']) < 1:
                body_error = "Please fill in the body"
            else:
                body_error = ""

            return render_template("new-post-page.html", title_error=title_error, body_error=body_error)

        
    if request.method == 'POST':
        new_blog = Blog(title = request.form['title'], body = request.form['body'])
        db.session.add(new_blog)
        db.session.commit()

        #body = request.form['body', type=str]
        #blog = Blog.query.get(body)
        #return blog.body
        #blogs = Blog.query.all()

        return redirect("/blog?id=" + str(new_blog.id))
        #return render_template("main-blog-page.html", blogs = blogs)
        

    return render_template("new-post-page.html")


@app.route('/blog')
def blog():
    
    blogs = Blog.query.all()
    

    if request.args.get("id", default=0, type=int) >= 1:
        id = request.args.get("id", default=0, type=str)
        blog = Blog.query.get(id)
        return render_template("individual-post-page.html", blog=blog)

    return render_template("main-blog-page.html", blogs = blogs)

if __name__ == '__main__':
    app.run()