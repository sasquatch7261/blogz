from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lettuce@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'letitsnow'


class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():

     allowed_routes=['login', '', 'blog', 'signup', 'index']

     if request.endpoint not in allowed_routes and 'username' not in session:

             return redirect('/login')


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

        new_blog = Blog(title = request.form['title'], body = request.form['body'], owner = User.query.filter_by(username=session['username']).first())
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

    if request.args.get("user", default=0, type=int) >= 1:
        user_id = request.args.get("user", default=0, type=str)
        user = User.query.get(user_id)
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('user-posts.html', user=user, blogs=blogs)

    return render_template("main-blog-page.html", blogs=blogs)

@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if not user:
            username_error = "Username does not exist"
            return render_template('login.html', username_error=username_error)
        elif user.password != password:
            password_error = "Pasword is incorrect"
            return render_template('login.html', password_error=password_error)
        elif user and password == user.password:
            session['username'] = username
            return redirect('/newpost')
        else:
            pass
    
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            existing_user_error = "Username already exists"
            return render_template('signup.html', existing_user_error=existing_user_error)
        elif len(username) == 0 or len(password) == 0 or verify == 0:
            error1 = "One or more fields are invalid" 
            return render_template('signup.html', error=error1)
        elif len(username) < 3:
            error4 = "Invalid username"
            return render_template('signup.html', error=error4)
        elif len(password) < 3:
            error5 = "Invalid password"
            return render_template('signup.html', error=error5)
        elif verify != password:
            error3 = "Passwords do not match"
            return render_template('signup.html', error=error3)
        else:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
            
            session['username'] = username

            return redirect('/newpost')

    return render_template('signup.html')


@app.route('/logout')
def logout():

    del session['username']
    return redirect('/blog')


@app.route('/')
def index():

    users = User.query.all()



    return render_template('index.html', users=users)


if __name__ == '__main__':
    app.run()


