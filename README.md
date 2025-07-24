# Flask Project

# 환경변수 설정 관련


# 데이터 타입

## User Table
```bash
- id: 유저 Primary Key 값
- email: email 값
- password: 비밀번호
- height: 신장
- weight: 몸무게
- isLogin: 유저 로그인 여부(세션 처리 방법 정립되면 없어도 되는 컬럼)
- created_at: 유저 회원가입 날짜
- updated_at: 유저 정보 수정 날짜
```

## Exercise Table
```bash
- id : 레코드 Primary Key 값
- user_id : user 테이블 foreign Key 값
- exercise_type: 운동 타입("pullup", "pushup", "situp", "squat")
- set_num: 세트 수
- reps: 1 세트 당 운동 반복 수
- created_at: 기록 생성 날짜
```

# Git 규칙
작업하는 자리의 주인의 성명으로 branch를 만들어서 commit push

# 페어프로그래밍 규칙

## 페어프로그래밍 짝
- 백엔드팀: 황유성, 김도연, 전유범(Dev/Ops 작업 없을 때 합류)
- 프론트엔드 팀: 임수열, 강두훈
- Dev/Ops: 전유범

# 250724
- routes 로 auth(인증), exercise(운동기록) 관심사 분리 -> 파일 확인 필수
    - 서버 띄우는 명령어는 다음으로 통일(프로젝트 루트 디렉터리에서)
    - `flask run`
- database 테이블 대소문자 구분 유의, 추후 데이터 조회할 때 테이블 명은 소문자로 통일.
- 각자 환경변수 설정 필요 -> .env 파일 확인 후 로컬 데이터에 맞춰서 환경변수 추가
    - 관련해서 .env 파일을 호스팅 서버에 있는 데이터베이스로 하고 싶은 경우 의사 전달바람.