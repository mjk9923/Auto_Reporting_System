from datetime import datetime
from dateutil.relativedelta import relativedelta
import pymysql

# 신규로 추가되는 고객사인지 판별하는 함수
# 기존 테이블에 데이터가 있다면 True 반환 / 없다면 False 반환
def exist_employee(cliname, clitype):
    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = """
        select count(*) as cnt from worklist where cliname='{0}' and clitype='{1}';
        """.format(cliname, clitype)
    print(sql)
    cursor.execute(sql)

    # 쿼리 실행 결과 result에 할당
    result = cursor.fetchall()
    print(result)

    db.close()

    # 만약 DB에 데이터가 있다면 True / 데이터가 없다면 False
    if result[0]['cnt'] >= 1:
        return True
    else:
        return False

# worklist 테이블에 데이터 추가
def insert_worklist_query(cliname, clitype):
    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = "INSERT INTO worklist (cliname, clitype) values('{0}','{1}');".format(cliname, clitype)
    print(sql)
    cursor.execute(sql)

    #쿼리 실행 결과 result에 할당
    #result = cursor.fetchall()
    db.commit()
    db.close()

