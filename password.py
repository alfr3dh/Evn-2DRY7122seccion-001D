import sqlite3
from flask import Flask, request

app = Flask(__name__)
db_name = 'test.db'

@app.route('/signup/v1', methods=['POST'])
def signup_v1():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS USER_PLAIN 
        (USERNAME TEXT PRIMARY KEY NOT NULL,
        PASSWORD TEXT NOT NULL);''')
    conn.commit()

    try:
        c.execute("INSERT INTO USER_PLAIN (USERNAME, PASSWORD) VALUES (?, ?)",
                  (request.form['username'], request.form['password']))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return "El usuario ya esta registrado."
    conn.close()
    return "registro exitoso"

def verify_plain(username, password):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    query = "SELECT PASSWORD FROM USER_PLAIN WHERE USERNAME = ?"
    c.execute(query, (username,))
    record = c.fetchone()
    conn.close()
    if not record:
        return False
    return record[0] == password

@app.route('/login/v1', methods=['POST'])
def login_v1():
    error = None
    if request.method == 'POST':
        if verify_plain(request.form['username'], request.form['password']):
            error = 'Acceso exitoso'
        else:
            error = 'Usuario o contrasena erronea'
    else:
        error = 'metodo erroneo'
    return error

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')