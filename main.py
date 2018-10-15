from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:MyPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def get_id():
        return id

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    blogID = request.args.get('id')
    if blogID is None:
        if request.method == 'POST':
            blog_title = request.form['title']
            blog_body = request.form['blog']
            new_blog = Blog(blog_title,blog_body)
            db.session.add(new_blog)
            db.session.commit()
    
        blogs = db.session.query(Blog)
        return render_template('myBlog.html',title="Build a Blog", blogs=blogs)
    else:
        blogs = db.session.query(Blog).filter_by(id = blogID)
        return render_template('entry.html',title="Build a Blog",blogs=blogs)
@app.route('/new_entry', methods=['POST','GET'])
def new_entry():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['blog']
        title_error = ""
        blog_error = ""
        if blog_title == "":
            title_error = "Please input a title."
        if blog_body == "":
            blog_error = "Please input text into the body."    
        new_blog = Blog(blog_title,blog_body)
        if title_error == "" and blog_error == "":
            db.session.add(new_blog)
            db.session.commit()
            blogs = db.session.query(Blog).filter_by(id = new_blog.id)
            return render_template('entry.html',title="Build a Blog", blogs=blogs)    
        else:
            return render_template('new_entry.html',title="Build a Blog",title_error=title_error,blog_error=blog_error)
    else:
        return render_template('new_entry.html',title="Build a Blog")

if __name__ == '__main__':
    app.run()