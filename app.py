from flask import Flask, render_template, request, redirect, url_for
from db import Database
import atexit

app = Flask(__name__)
db = Database()

atexit.register(db.close)

# TODO: Router 및 Controller 구현 필요

@app.route('/', methods=['GET'])
def login_page():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
