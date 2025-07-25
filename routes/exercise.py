from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def mypage():
    # 마이페이지 조회
    records = db.get_mypage(id)
    return render_template('mypage.html', record=records)
    

@exercise_bp.route('/workout', methods=['GET'])
def login_page():
    return render_template('workout.html')

@exercise_bp.route('/save', methods=['POST'])
def record():
    exercise_type = request.form.get('exercise_type')
    set_num = request.form.get('set')
    rep_num = request.form.get('rep')
    
    if  db.save_exer_record(exercise_type, set_num, rep_num):
        redirect(url_for('mypage'))
    else:
        print(f"운동 이력 작성 중 문제 발생")