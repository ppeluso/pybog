import sqlite3 as sql
from werkzeug.security import check_password_hash
import os
import markdown
from flask import Markup
from datetime import datetime
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, 'data/data.db')

class Post(object):
    def __init__(self, title, text, date, categories, draft = 0):
        self.title = title 
        self.text = text 
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') 
        self.draft = draft
        self.categories = categories
    def to_sql(self):
        post_data = (self.title, self.text, self.date, self.draft, repr(self.categories.split(',')))
        conn = sql.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO posts (title, post, post_date, draft, categories) VALUES (?, ? , ?, ?, ?)", post_data)
        conn.commit()
        conn.close()
    def update_post(self, id):
        info = (id, self.title, self.text, self.date, repr(self.categories.split(',')), self.draft)
        conn = sql.connect(DATABASE)
        c = conn.cursor() 
        c.execute("REPLACE INTO posts (id, title, post, post_date, categories, draft) VALUES (?, ? , ?, ?, ?, ?);", info)
        conn.commit()
        conn.close()
    def md_to_html(self):
        self.text = markdown.markdown(self.text)
    def markup(self):
        self.text = Markup(markdown.markdown(self.text))


class AdminInterface():
    def __init__(self):
        pass
    def get_posts(self):
        conn = sql.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT post FROM posts;")
        posts = c.fetchall()
        conn.close()
        return posts
    def get_titles(self):
        conn = sql.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT title FROM posts;")
        title = c.fetchall()
        conn.close()
        return title

def url_to_title(url):
    url = url.lower()
    url = url.replace("_", " ")
    return url
def title_to_url(title):
    title= title.lower()
    title = title.replace(" ", "_")
    return title

def get_post_title_from_url(title):
    title = (title,)
    conn = sql.connect(DATABASE)
    c = conn.cursor()
    c.execute("select title, post, id, categories from posts where title = ?  collate nocase;",title)
    info = c.fetchall()
    conn.close()
    return info

def get_non_drafts():
    conn = sql.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * from posts where draft IS NOT 1 ORDER BY datetime(post_date) DESC;")    
#c.execute("SELECT title, post, post_date, categories FROM posts where draft IS NOT 1 ORDER BY datetime(post_date) DESC;")
    info = c.fetchall()
    conn.close()
    return info

def get_user_pass():
    conn = sql.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT username, password FROM admin;")
    info = c.fetchall()
    return info
def check_pass(password, hash_pass):
    return check_password_hash(password, hash_pass)

if __name__ == '__main__':
    print(get_non_drafts())

