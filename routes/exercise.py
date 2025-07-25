from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def workout():
    # 마이페이지 조회
    records = db.get_mypage(id)
    return render_template('mypage.html', record=records)
    

@exercise_bp.route('/', methods=['GET'])
def login_page():
    return render_template('mypage.html')