from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
import atexit
from db import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key'
db = Database() # database 연결

atexit.register(db.close)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST": # 클라이언트의 요청이 데이터를 처리해주세요(POST)이라면,
        email = request.form.get('email')
        password = request.form.get('password')
        if {"email":email, "password":password} in db.read_user_list(): # DB에 이메일, 패스워드가 매칭됐을 때
            print(db.select_id_for_session(email))
            session['id'] = db.select_id_for_session(email)
            return render_template_string("성공")
        else: # DB에 이메일, 패스워드가 없을 때
            #flash()
            return redirect(url_for('login'))
    return render_template('login.html')
#         if user:
#             session['email'] = email
#             return redirect(url_for('DashBoard'))
#         else:
#             flash('로그인 실패: 아이디 또는 비밀번호가 잘못되었습니다.')
#             return redirect(url_for('login'))
#     # GET 요청 시 로그인 폼 보여주기
#     return render_template('login.html')

# @app.route("/DashBoard")
# def DashBoard():
#     return render_template('DashBoard.html')

@app.route("/SignUp",methods = ['GET','POST'])
def SignUp(): # 회원가입 
    if request.method == "POST":
        agree = request.form.get("agree")
        email = request.form.get("email")
        password = request.form.get("password")

        if not agree: # 
            flash("약관에 동의해야 회원가입이 가능합니다.")
            return redirect(url_for('SignUp'))
        is_success, result_message = db.create_account(email, password)
        if is_success:
            return render_template('login.html',result_message = result_message)
        else:
            print(result_message)
            return render_template("signup.html",result_message=result_message)
    return render_template('signup.html')
@app.route('/workout')
def workout():
    # 마이페이지 조회
    records = db.get_mypage(id)
    return render_template('mypage.html', record=record)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
