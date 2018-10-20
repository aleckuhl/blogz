from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:12345@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'asfii@3lazo'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def get_id():
        return id

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self,username,password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')
@app.route('/', methods=['POST', 'GET'])
def index():
    userID = request.args.get('user')
    blogID = request.args.get('id')
    blog_owner = User.query.filter_by(id=userID).first()
    blogs = []
    username = ""
    if blogID is None:
        if request.method == 'POST':
            blog_title = request.form['title']
            blog_body = request.form['blog']
            new_blog = Blog(blog_title,blog_body)
            db.session.add(new_blog)
            db.session.commit()
        user = User.query.filter_by(username=session['user']).first()
        if user != None and userID == None:
            blogs = Blog.query
        else:  
            blogs = Blog.query.filter_by(owner=blog_owner)  
        return render_template('myBlog.html',title="Blogz", blogs=blogs, userid=userID,user=username)
    else:
        blogs = db.session.query(Blog).filter_by(id = blogID)
        return render_template('entry.html',title="Blogz",blogs=blogs,user=username)
@app.route('/home') 
def home():
    users = User.query
    return render_template('index.html', title = "Blogz", users=users)       
@app.route('/new_entry', methods=['POST','GET'])
def new_entry():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blog']
        owner = User.query.filter_by(username=session['user']).first()
        title_error = ""
        blog_error = ""
        if blog_title == "":
            title_error = "Please input a title."
        if blog_body == "":
            blog_error = "Please input text into the body."    
        new_blog = Blog(blog_title,blog_body,owner)
        if title_error == "" and blog_error == "":
            db.session.add(new_blog)
            db.session.commit()
            blogs = db.session.query(Blog).filter_by(id = new_blog.id)
            return render_template('entry.html',title="Blogz", blogs=blogs)    
        else:
            return render_template('new_entry.html',title="Blogz",title_error=title_error,blog_error=blog_error)
    else:
        return render_template('new_entry.html',title="Blogz")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_flag = False
        user_error = ""
        password_error = ""
        user = User(username,password)
        user_check = User.query.filter_by(username=username).first()
        if user_check != None:
            if user_check.password != password:
                password_error = "Incorrect Password"
        if user_check == None:
            user_error = "Username does not exist"    
        if user_check != None:    
            if user_check.password == password:
                session['user'] = username
                login_flag = True
               
        if login_flag == True:
            return redirect('/new_entry')        
        else:
            return render_template('login.html',title='Blogz',user_error=user_error,password_error=password_error)
    else:
        return render_template('login.html',title ='Blogz')        
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        user = User(username,password)
        user_check = User.query.filter_by(username=username).first()
        username_error = ""
        password_error = ""
        verify_error = ""
        
        if len(username) < 3:
            username_error = "Your username must be at least 3 characters in length."   
        if username == "":
            username_error = "Your username field can't be blank."
        if password != verify or verify == "":
            verify_error = "Your passwords must match."
            password_error = "Your passwords must match."     
        if len(password) < 3:
            password_error = "Your password must be at least 3 characters in length"
        if password == "":
            password_error = "Your password can't be blank." 

        if user_check != None and username == user_check.username:
            username_error = "Username already exists" 
        if username_error == "" and password_error == "" and verify_error == "": 
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            return redirect('/new_entry')
        else:
            return render_template('signup.html', title = 'Blogz', password_error=password_error,username_error=username_error,verify_error=verify_error)
    else:
        return render_template('signup.html',title = 'Blogz')
@app.route("/logout")
def logout():
    del session['user']
    return redirect('/')
if __name__ == '__main__':
    app.run()