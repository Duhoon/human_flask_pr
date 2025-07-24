import pymysql
import os
from pymysql import Error, IntegrityError
from dotenv import load_dotenv

class Database:
    def __init__(self):  
        self.connection = None
        try:
            self.connection = pymysql.connect(
                host='localhost',  # 로컬 PC
                port=3306,
                database='test',  # test 데이터베이스 사용
                user='root',
                password='Yousung0528!',  # mariadb 설치 당시의 패스워드, 실제 환경에서는 보안을 위해 환경변수 등을 사용
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor   # 쿼리 결과를 딕셔너리로 변환
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 중 오류 발생: {e}")
    
    # TODO: DB 컨넥션 및 Model 관련 작업 필요
    def create_account(self, email, password) -> bool:
        if self.connection is None: # DB에 연결이 없을 때,
            return False, "데이터 베이스 연결이 되지 않았습니다."
        try:
            with self.connection.cursor() as c:  # cursor()는 함수이므로 () 필요
                query = """INSERT INTO `user` (email, password) VALUES (%s, %s);"""
                c.execute(query, (email, password))
            self.connection.commit()
            return True,"DB에 데이터가 성공적으로 저장되었습니다."
        
        except IntegrityError as ie:  # 중복 이메일 등 무결성 오류 처리
            return False, f"중복된 이메일이 들어왔습니다. {ie}"
        
        except Exception as e:  # 그 외 예외 처리
            return False, f"알 수 없는 오류 발생: {e}" 
    
    # Read Account List
    def read_user_list(self):
        try:
            if self.connection is None: # 연결이 되지 않았을 때,
                print("데이터 베이스 연결이 되지 않았습니다.")
                return []
            with self.connection.cursor() as c:
                query = """
                    SELECT email, password FROM USER
                    """
                c.execute(query)
                return c.fetchall()
        except Exception as e:
            print(f"데이터 조회를 실패했습니다.", {e})
            return []
        
    def select_id_for_session(self, email): #데이터 베이스에서 Seesion을 위한 ID 추출
        try:
            if self.connection is None:
                print("데이터 베이스 연결이 되지 않았습니다.")
                return None
            with self.connection.cursor() as c:
                query = """
                        SELECT id FROM USER WHERE email = %s
                        """
                c.execute(query, (email,))
                print(type(c.fetchone()['id']))
                return c.fetchone()['id']
        except Error as e:
            print(f"로그인 실패했습니다. {e}")
            return None
    def get_mypage(self, id):
        self.id = id
        """마이페이지 조회"""
        try:
            if self.connection is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with self.connection.cursor() as cursor:
                query = """
                    SELECT 
                        ID
                        , password 
                        , HEIGHT
                        , WEIGHT
                        , CREATED_AT
                        , UPDATED_AT
                    FROM USER
                    WHERE ID = %s
                """
                cursor.execute(query, (id,))
                record = cursor.fetchall()
            return record
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return False
    
    
    def save_exer_record(self, weight, exercise_type, set_num, rep):
        try:
            if self.connection is None:
                print("Not connected.")
                return False
            
            with self.connection.cursor() as cursor:
                query = """
                INSERT INTO EXERCISE (exercise_type, set_num, reps)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (exercise_type, set_num, rep))
                
            self.connection.commit()
            print("기록이 저장되었습니다.")
            return True
        except Error as e:
            print(f"기록 저장 중 오류 발생: {e}")
            return False
        
    def get_record(self, user_id):
        try:
            if self.connection is None:
                print("Not connected.")
                return False
            
            with self.connection.cursor() as cursor:
                # 사용자 정보 조회
                cursor.execute("SELECT name, height, weight FROM USER WHERE user_id = %s",
                               (user_id,))
                user = cursor.fetchall()
                
                # 운동 기록 조회
                query = """
                SELECT * FROM EXERCISE
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s                
                """
                cursor.execute(query, (user_id,))
                exercise = cursor.fetchall()
                
        except Error as e:
            print(f"기록 저장 중 오류 발생: {e}")
            return False
        
        
    def close(self):
        # 데이터베이스 연결 종료
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")
