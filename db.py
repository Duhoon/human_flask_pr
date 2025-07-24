import pymysql
import os
from pymysql import Error, IntegrityError
from dotenv import load_dotenv



load_dotenv()

class Database:
    def __init__(self):  
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',  # 로컬 PC
                port=3306,
                database='test',  # test 데이터베이스 사용
                user='root',
                password='qwer1234',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor   # 쿼리 결과를 딕셔너리로 변환
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")
    
    # TODO: DB 컨넥션 및 Model 관련 작업 필요
<<<<<<< HEAD
    def create_account(self, email, password) -> bool:
        if self.connection is None: # DB에 연결이 없을 때,
            print("데이터 베이스 연결이 되지 않았습니다.")
            return False
        with self.connection.cursor as c:
            try: # 중복 이메일이 들어왔을 때,
                query = """INSERT INTO USER (email, password)
                        VALUES (%s, %s);"""
                c.execute(query, (email, password))
            except IntegrityError as ie: # 중복 이메일을 다시 처리를 해줘야하는 문
                print(f"중복된 이메일이 들어왔습니다.", {ie})
            self.connection.commit()
            print("DB에 데이터가 성공적으로 저장되었습니다.")
            return True
    
    # Read Account List
    def read_user_list(self):
        if self.connection is None:
            print("데이터 베이스 연결이 되지 않았습니다.")
            query = """
                SELECT (email, password) FROM USER
                """

=======
    
    def close(self):
        # 데이터베이스 연결 종료
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")
>>>>>>> 34c7056e1f6d55c3b16928a76816d541bd3edbb7
