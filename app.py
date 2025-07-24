from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, current_app
import atexit
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.exercise import exercise_bp

load_dotenv() # .env 파일 환경설정 불러오기

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.register_blueprint(auth_bp)
app.register_blueprint(exercise_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)