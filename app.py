from flask import Flask, render_template, url_for, request, redirect, Markup, session, send_from_directory 
import markdown
import sqlite3 as sql
from models import *
from datetime import datetime
import random
import os
from functools import wraps
app = Flask(__name__)

app.secret_key = str(random.random())

dir,_ = os.path.split(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(dir, "uploads")



def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session["logged_in"] == True:
            return redirect(url_for('admin_login'))
        else:
            return f(*args, **kwargs)
    return decorated

@app.route("/", methods= ["GET"])
def index():
    info = get_non_drafts()
    print(info)
    posts = [Post(i[1], i[2], i[3], eval(i[5])) for i in info]
    for x in posts:
        x.markup()
    return render_template("index.html", posts = posts)
    
@app.route("/admin")
@login_required
def admin():
    adm = AdminInterface()
    titles = adm.get_titles()
    links = [ "/admin/" + title_to_url(i[0]) for i in titles ]
    t_and_l = list(zip(links, titles))
    return render_template('admin.html', tl = t_and_l)

@app.route("/admin/newpost",methods=['GET','POST'])
@login_required
def new_post():

    if request.method == 'POST' and request.form.get("title") and request.form.get("text"):
        title = request.form.get('title')
        text = request.form.get('text')
        draft = request.form.get('check')
        date = str(datetime.now())
        categories = request.form.get("categories")
        categories = categories
        post = Post(title, text, date, categories, draft)
        post.to_sql()
        return redirect(url_for('admin'))


    return render_template('admin_newpost.html')
@app.route("/admin/<post_title>", methods = ['GET', 'POST'])
@login_required
def post_edit(post_title):
    title = url_to_title(post_title)
    info = get_post_title_from_url(title)
    print(info)
    org_title = info[0][0]
    org_post = info[0][1]
    id = info[0][2]
    cat = eval(info[0][3])

    if request.method == 'POST' and( request.form.get('title') or request.form.get('text') or request.form.get('categories')):
        title = request.form.get('title')
        text = request.form.get('text')
        draft = request.form.get('check')
        categories = request.form.get('categories')
        print(categories)
        date = str(datetime.now())
        post = Post(title, text, date,categories, draft)
        post.update_post(id)
        return redirect(url_for('admin'))
    
    return render_template("edit_post.html", title = org_title, post = org_post, post_title = post_title, categories = cat)

@app.route('/login', methods= ['POST', 'GET'])
def admin_login():
    try:
        if session['logged_in'] == True:
            return redirect(url_for("admin"))
        
    except KeyError:
        pass
    x = get_user_pass()
    user = x[0][0]
    hash_pass = x[0][1]
    if request.method == 'POST':
        user_try = request.form.get('username')
        pass_try = request.form.get('password')
        if (check_pass(hash_pass, pass_try)) and user_try == user:
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('index'))
    return render_template("login.html")
@app.route('/logout', methods= ["GET"])
def admin_logout():
    print("hello")
    session['logged_in'] = False
    return ("see ya around")

@app.route('/admin/photos', methods= ["GET", "POST"])
def admin_photo():
    print(request.path)
    filelist = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    if request.method == "POST" and request.form.get("delete"):
        os.remove(os.path.join(UPLOAD_FOLDER,request.form["delete"]))
        redirect(url_for('admin_photo'))

    if request.method == "POST" and request.form.get("file"):
        file = request.files['file']
    # Check if the file is one of the allowed types/extensions
        if file:
            filename = file.filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('index'))
    return render_template("admin_photo.html", filenames = filelist)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)

if __name__ == "__main__":

    app.run(debug = True)
