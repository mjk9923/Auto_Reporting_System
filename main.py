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
    return render_template('work_com_request.html')

@app.route('/work_com_request')
def work_com_request():
    return render_template('work_com_request.html')

# 장애 내역 등록 페이지 클릭
@app.route('/work_com_request_click', methods=["GET", "POST"])
def work_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    occur = request.form.get("occur", type=str)
    action = request.form.get("action", type=str)
    charge = request.form.get("charge", type=str)
    perform = request.form.get("perform", type=str)
    day = request.form.get("day", type=str)
    comment = request.form.get("comment", type=str)
 
    # 기존 고객 정보와 일치하면 데이터 추가 진행
    #if not exist_employee(cliname, clitype):
    insert_logs_query(cliname, clitype, occur, action, charge, perform, day, comment)


    return render_template("client_com_pop.html")



# 고객사 등록 페이지 라우팅
@app.route('/client_com_request')
def client_com_request():
    return render_template('client_com_request.html')

# 고객사 등록 페이지 클릭
@app.route('/client_com_request_click', methods=["GET", "POST"])
def client_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    

    # 만약 테이블에 해당 고객사에 대한 데이터가 존재하지 않는다면 추가
    if not exist_employee(cliname, clitype):
        insert_worklist_query(cliname, clitype)

    return render_template("client_com_pop.html")


# 고객사 등록 내역 조회
@app.route("/client_log", methods=["POST", "GET"])
def client_log():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')


    # 고객사 별로 연간, 월간 데이터 업데이트
    #update_stat_query()

    result = select_worklist_query_whole()

    return render_template("client_log.html", data=result, client_type=year)



# log 테이블에 휴가 신청에 대한 내역 추가
    insert_log_query(cliname, clitype, occur, action, charge, perform, day, comment)

if __name__ == '__main__':
    app.run(host="192.168.219.29", port="9730", debug=True)