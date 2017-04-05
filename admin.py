from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sql
import os
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DATABASE = os.path.join(APP_ROOT, 'data/data.db')
class AdminUser():

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    def to_sql(self):
        info = (self.username, self.pw_hash)
        conn = sql.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO admin VALUES (?, ?) ;', info)
        conn.commit()
        conn.close()
if __name__ == '__main__':
    admin = AdminUser("ppeluso", "lirr3692")
    admin.to_sql()

