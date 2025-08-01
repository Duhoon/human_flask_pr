from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database
from collections import defaultdict
import json

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def mypage():
    # 마이페이지 조회
    # 해당되는 유저 id 로그인이 되어있어야 mypage로 갈 수 있게,
    id_now = session.get('id',None)
    if id_now:
        records = db.get_mypage(id_now)
        profile = db.get_mypage_profile(id_now)
        # 최근 7일간 운동 종류별 누적 횟수
        summary = defaultdict(int)
        
        for record in records:
            ex_type = record.get("exercise_type")
            reps = record.get("REPS", 0)
            
            if ex_type:
                summary[ex_type] += reps
                
        total = total_nums(records)
                
        print(json.dumps(list( total.keys() )))
        print(json.dumps(list( total.values() )))
        return render_template('mypage.html', record=records, summary = summary, profile=profile, axis=json.dumps(list(total.keys())), data=json.dumps(list(total.values())))
    else:
        return redirect(url_for('index'))
    
@exercise_bp.route('/workout', methods=['GET'])
def workout():
    user_id = session.get('id', None)
    if user_id == None: # 세션이 없으면
        return redirect(url_for('index'))
    return render_template('workout.html')

@exercise_bp.route('/save', methods=['POST'])
def save():
    user_id = session.get('id',None)
    if user_id == None: # 세션이 없으면,
        return redirect(url_for('index'))
    exercise_type = request.form.get('exercise_type')
    set_num = request.form.get('set')
    rep_num = request.form.get('rep')
    
    if db.save_exer_record(user_id, exercise_type, set_num, rep_num): # 성공적으로 값이 들어갈 때,
        return redirect(url_for('exercise.mypage')) # 성공적으로 값이 들어가면, redirect -> mypage
    else:
        print(f"운동 이력 작성 중 문제 발생")
        return redirect(url_for('exercise.workout')) 
    
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
            
def daily_exercise_type(records):
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
    
    return ex_type_summary

def total_nums(records):
    # 중첩 딕셔너리: 날짜 → 운동 → 반복수 누적
    total = {}

    for record in records:
        ex_type = record.get("exercise_type")
        
        if ex_type is None:
            continue

        date = record.get("created_at")
        date_str = date.strftime('%Y-%m-%d')  # 날짜 문자열로 정제
        set_num = int(record.get("set_num"))
        reps = int(record.get("REPS", 0))

        if total.get(date_str):
            total[date_str] += set_num * reps
        else :
            total[date_str] = set_num * reps
    
    return total

@exercise_bp.route('/', methods=['GET'])
def login_page():
    return render_template('mypage.html')

