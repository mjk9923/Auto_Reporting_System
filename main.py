import csv
from flask import *
from mysql import *
# import smtplib
# from email.mime.text import MIMEText
# import pandas as pd
#import numpy as np

app = Flask(__name__)

# 장애 내역 등록 페이지 라우팅
@app.route('/chanwoojjangjjangman')
def chanwoojjangjjangman():
    return render_template('service/work_com_request.html')

@app.route('/work_com_request')
def work_com_request():
    return render_template('service/work_com_request.html')

# 장애 내역 등록 페이지 클릭
@app.route('/work_com_request_click', methods=["GET", "POST"])
def work_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    occur = request.form.get("occur", type=str)
    nmtime = request.form.get("nmtime", type=int)
    action = request.form.get("action", type=str)
    charge = request.form.get("charge", type=str)
    perform = request.form.get("perform", type=str)
    day = request.form.get("day", type=str)
    comment = request.form.get("comment", type=str)
    # 기존 고객 정보와 일치하면 데이터 추가 진행
    #if not exist_employee(cliname, clitype):
    insert_logs_query(cliname, clitype, occur, nmtime, action, charge, perform, day, comment)

    return render_template("sub/client_com_pop.html")


# 고객사 등록/내역조회 페이지 라우팅
@app.route('/client_com_request', methods=["POST", "GET"])
def client_com_request():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')

    result = select_worklist()
    return render_template('service/client_com_request.html', data=result, client_type=year)

# 고객사 등록 페이지 클릭
@app.route('/client_com_request_click', methods=["GET", "POST"])
def client_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    
    # 만약 테이블에 해당 고객사에 대한 데이터가 존재하지 않는다면 추가
    if not exist_employee(cliname, clitype):
        insert_worklist_query(cliname, clitype)

    return render_template("sub/client_com_pop.html")



# 직원별 휴가 일수 연별 통계
# 테스트
@app.route("/year_stat2", methods=["POST", "GET"])
def year_stat2():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')
    if request.method == 'POST':
        year = request.form["year"]

    # stat 테이블 전체 조회해서 전체 직원 정보 추출
    for row in select_worklist():   
       
        # 직원 별로 연차, 반차 데이터를 업데이트
        result_update = update_stat_query(row['cliname'], row['clitype'])
    
    result = select_worklist()
    return render_template("service/year_stat.html", data=result, current_year=year)

# log 테이블에 휴가 신청에 대한 내역 추가
    #insert_log_query(cliname, clitype, occur, action, charge, perform, day, comment)

if __name__ == '__main__':
    app.run(host="192.168.219.29", port="9730", debug=True)