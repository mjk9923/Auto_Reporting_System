#!/bin/python3
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
    clitype = request.form.get("clitype", type=str)
    occur = request.form.get("occur", type=str)
    nmtime = request.form.get("nmtime", type=int)
    action = request.form.get("action", type=str)
    charge = request.form.get("charge", type=str)
    perform = request.form.get("perform", type=str)
    day = request.form.get("day", type=str)
    comment = request.form.get("comment", type=str)

    # 기존 고객 정보와 일치하면 데이터 추가 진행
    if insert_check_data(cliname,clitype):
        insert_logs_query(cliname, clitype, occur, nmtime, action, \
        charge, perform, day, comment)

    return render_template("sub/client_com_pop.html")

# 고객사 등록/내역조회 페이지 라우팅
@app.route('/client_com_request', methods=["POST", "GET"])
def client_com_request():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')

    for row in select_worklist():   
       
        # 고객사 총 건수 업데이트
        result_update = update_stat_all_date(row['cliname'], row['clitype'])
    
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


# 고객별 작업 일수 연별 통계
@app.route("/year_stat", methods=["POST", "GET"])
def year_stat():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')
    if request.method == 'POST':
        year = request.form["year"]

    print(year)

    result = select_stat_year_date(year)
    return render_template("service/year_stat.html", data=result, current_year=year)

# 고객별 작업 일수 월별 통계
@app.route("/mon_stat", methods=["POST", "GET"])
def mon_stat():
    dt_now = datetime.now()
    year_month = dt_now.strftime('%Y-%m')
    year = dt_now.strftime('%Y')
    month = dt_now.strftime('%m')
    if request.method == 'POST':
        year_month = request.form["month"]
        year = year_month.split('-')[0]
        month = year_month.split('-')[1]
    
    print(year)
    print(month)
    
    result = select_stat_mon_date(year,month)
    return render_template("service/mon_stat.html", data=result, current_year=year, current_month=month)

# 장애 내역 관리 페이지
# 전체 작업(logs) 내역 페이지
@app.route("/client_logs", methods=["POST", "GET"])
def client_logs():
    dt_now = datetime.now()
    year_month = dt_now.strftime('%Y-%m')
    year = dt_now.strftime('%Y')
    month = dt_now.strftime('%m')
    #filter_type = "전체"
    if request.method == 'POST':
        year_month = request.form["month"]
        #filter_type = request.form["filter_type"]
        year = year_month.split('-')[0]
        month = year_month.split('-')[1]

    result = select_stat_client_logs(year,month)
    return render_template("service/client_logs.html", data=result, current_year=year, current_month=month)

# 전체 작업(logs) 내역 관리 상세 페이지
@app.route("/client_logs_detauled", methods=["POST", "GET"])
def client_logs_detauled():
    id = request.form['getid']
    cliname = request.form['cliname']

    result = select_stat_logs_id(id)
    return render_template("service/client_logs_detauled.html", data=result, cliname=cliname ,getid=id)

### 장애 내역 관리 테스트 페이지
@app.route("/delid_click", methods=["POST", "GET"])
def delid_click():
    id = request.form['getid']
    delete_logs(id)

    return render_template("sub/del_complet.html")


##### 테스트
## 명준테스트
@app.route('/mj_test')
def mj_test():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')

    for row in select_worklist():   
       
        # 고객사 총 건수 업데이트
        result_update = update_stat_all_date(row['cliname'], row['clitype'])
    
    result = select_worklist()
    return render_template('test/mj_test2.html',data=result, client_type=year)

## 찬우테스트
@app.route('/cw_test')
def cw_test():
    return render_template('test/내역입력.html')

## 내역 수정 테스트
@app.route('/test3', methods=["GET", "POST"])
def test3():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    occur = request.form.get("occur", type=str)
    nmtime = request.form.get("nmtime", type=int)
    action = request.form.get("action", type=str)
    charge = request.form.get("charge", type=str)
    perform = request.form.get("perform", type=str)
    day = request.form.get("day", type=str)
    comment = request.form.get("comment", type=str)

    insert_logs_query(cliname, clitype, occur, nmtime, action, charge, \
    perform, day, comment)

    return render_template("test/worklist_test.html")



if __name__ == '__main__':
    app.run(host="192.168.219.29", port="9730", debug=True)