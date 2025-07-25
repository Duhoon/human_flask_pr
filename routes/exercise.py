from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database
from collections import defaultdict

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def mypage():
    # 마이페이지 조회
    records = db.get_mypage(id)
    profile = db.get_mypage_profile(id)
    # 최근 7일간 운동 종류별 누적 횟수
    summary = defaultdict(int)
    
    for record in records:
        ex_type = record.get("exercise_type")
        reps = record.get("REPS", 0)
        
        if ex_type:
            summary[ex_type] += reps
            
    return render_template('mypage.html', record=records, summary = summary, profile=profile)

@exercise_bp.route('/workout', methods=['GET'])
def workout():
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
        
def daily_exercise():
    # 마이페이지 조회
    records = db.get_mypage(id)
    
    # 중첩 딕셔너리: 날짜 → 운동 → 반복수 누적
    daily_summary = defaultdict(lambda: defaultdict(int))

    for record in records:
        date = record.get("created_at")
        if date is None:
            continue

        date_str = date.strftime('%Y-%m-%d')  # 날짜 문자열로 정제
        ex_type = record.get("exercise_type")
        reps = record.get("REPS", 0)

        if ex_type:
            daily_summary[date_str][ex_type] += reps
            
def daily_exercise_type():
    # 마이페이지 조회
    records = db.get_mypage(id)
    
    # 중첩 딕셔너리: 날짜 → 운동 → 반복수 누적
    ex_type_summary = defaultdict(lambda: defaultdict(int))

    for record in records:
        ex_type = record.get("exercise_type")
        
        if ex_type is None:
            continue

        date = record.get("created_at")
        date_str = date.strftime('%Y-%m-%d')  # 날짜 문자열로 정제
        reps = record.get("REPS", 0)

        if date_str:
            ex_type_summary[ex_type][date_str] += reps
        

@exercise_bp.route('/', methods=['GET'])
def login_page():
    return render_template('mypage.html')

