import pymysql
import os
from pymysql import Error
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
    
    
    def close(self):
        # 데이터베이스 연결 종료
        if self.connection:
            self.connection.close()
            print("MariaDB 연결이 종료되었습니다.")