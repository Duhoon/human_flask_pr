from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string, Blueprint
from dbconnection import Database
from collections import defaultdict

db = Database()

exercise_bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@exercise_bp.route('/mypage')
def workout():
    # 마이페이지 조회
    records = db.get_mypage(id)
    
    # 최근 7일간 운동 종류별 누적 횟수
    summary = defaultdict(int)
    
    for record in records:
        ex_type = record.get("exercise_type")
        reps = record.get("REPS", 0)
        
        if ex_type:
            summary[ex_type] += reps
            
    return render_template('mypage.html', record=records, summary = summary)

@exercise_bp.route('/', methods=['GET'])
def login_page():
    return render_template('mypage.html')