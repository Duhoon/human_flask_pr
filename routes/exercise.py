from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database
from collections import defaultdict

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def mypage():
    # 마이페이지 조회
    # 해당되는 유저 id 로그인이 되어있어야 mypage로 갈 수 있게,
    id_now = session.get('id',None)
    if id_now:
        records = db.get_mypage(id_now)
        
        # 최근 7일간 운동 종류별 누적 횟수
        summary = defaultdict(int)
        
        for record in records:
            ex_type = record.get("exercise_type")
            reps = record.get("REPS", 0)
            
            if ex_type:
                summary[ex_type] += reps
                
        return render_template('mypage.html', record=records, summary = summary)
    else:
        return redirect(url_for('index'))
    
@exercise_bp.route('/workout', methods=['GET'])
def workout():
    if session.get('id',None) == None: # 세션이 없으면
        return redirect(url_for('index'))
    return render_template('workout.html')

@exercise_bp.route('/save', methods=['POST'])
def record():
    if session.get('id',None) == None: # 세션이 없으면,
        return redirect(url_for('index'))
    exercise_type = request.form.get('exercise_type')
    set_num = request.form.get('set')
    rep_num = request.form.get('rep')
    
    print(db.save_exer_record(exercise_type,set_num,rep_num))
    if db.save_exer_record(exercise_type, set_num, rep_num): # 성공적으로 값이 들어갈 때,
        redirect(url_for('mypage')) # 성공적으로 값이 들어가면, redirect -> mypage
    else:
        print(f"운동 이력 작성 중 문제 발생")