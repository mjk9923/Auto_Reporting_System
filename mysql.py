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
    
# logs 테이블에 데이터 추가
def insert_logs_query(cliname, clitype, occur, nmtime, action, charge, perform, day, comment):
    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = "INSERT INTO logs (cliname, clitype, occur, nmtime, action, charge, perform, day, comment) values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(cliname, 
                                                                                                                                                              clitype, 
                                                                                                                                                              occur,
                                                                                                                                                              nmtime, 
                                                                                                                                                              action, 
                                                                                                                                                              charge, 
                                                                                                                                                              perform, 
                                                                                                                                                              day, 
                                                                                                                                                              comment)
    print(sql)
    cursor.execute(sql)

    #쿼리 실행 결과 result에 할당
    #result = cursor.fetchall()
    db.commit()
    db.close()


#######################################################################################################################
#############################3########################################################################################
######################################################################################################################


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

# worklist 테이블 전체 데이터 조회
def select_worklist_query_whole():
    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = "select * from worklist order by cliname;"
    print(sql)
    cursor.execute(sql)

    # 쿼리 실행 결과 result에 할당
    result = cursor.fetchall()
    print(result)

    db.close()

    return result


# worklist 테이블 고객사 연간 데이터 조회
def select_log_query_year_employee(cliname,clitype):
    # 오늘 날짜
    dt_now = datetime.now()
    end_month = dt_now - relativedelta(months=0)
    print(end_month.strftime('%Y-%m'))

    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = "SELECT {0}, {1}, COUNT(*) as all_date FROM logs GROUP BY {0}, {1} ORDER BY all_date DESC;".format(
        cliname,
        clitype
    )
        
    print(sql)
    cursor.execute(sql)

    # 쿼리 실행 결과 result에 할당
    result = cursor.fetchall()
    print(result)

    db.close()

    return result

# worklist 테이블에 데이터 변경
def update_stat_query(cliname, clitype, all_data, mon_data):
    db = pymysql.connect(
        host='192.168.219.29', port=3306, user='dev_cw', password='cksdn3839!', db='STW', charset='utf8mb4'
    )

    # DictCursor: 딕셔너리 형태 / Cursor: 튜플 형태
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # DB 실행
    sql = "update worklist set all_data={0}, mon_data={1} where cliname='{2}' and clitype='{3}';".format(all_data,
                                                                                                     mon_data,
                                                                                                     cliname,
                                                                                                     clitype)
    print(sql)
    cursor.execute(sql)
    db.close()


    