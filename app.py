from flask import Flask, render_template, request, redirect, url_for
from db import Database
import atexit

app = Flask(__name__)
db = Database()

atexit.register(db.close)

# TODO: Router 및 Controller 구현 필요

@app.route('/workout')
def workout():
    # 마이페이지 조회
    records = db.get_mypage(id)
    return render_template('mypage.html', record=record)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)