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
    nmtime = request.form.get("nmtime", type=int)
    action = request.form.get("action", type=str)
    charge = request.form.get("charge", type=str)
    perform = request.form.get("perform", type=str)
    day = request.form.get("day", type=str)
    comment = request.form.get("comment", type=str)
 
    # 기존 고객 정보와 일치하면 데이터 추가 진행
    #if not exist_employee(cliname, clitype):
    insert_logs_query(cliname, clitype, occur, nmtime, action, charge, perform, day, comment)


    return render_template("client_com_pop.html")


# 고객사 등록/내역조회 페이지 라우팅
@app.route('/client_com_request', methods=["POST", "GET"])
def client_com_request():
    dt_now = datetime.now()
    year = dt_now.strftime('%Y')


    # 고객사 별로 연간, 월간 데이터 업데이트
    #update_stat_query()

    result = select_worklist_query_whole()
    return render_template('client_com_request.html', data=result, client_type=year)

# 고객사 등록 페이지 클릭
@app.route('/client_com_request_click', methods=["GET", "POST"])
def client_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    

    # 만약 테이블에 해당 고객사에 대한 데이터가 존재하지 않는다면 추가
    if not exist_employee(cliname, clitype):
        insert_worklist_query(cliname, clitype)

    return render_template("client_com_pop.html")



# 직원별 휴가 일수 월별 통계
@app.route("/table_stat_month", methods=["POST", "GET"])
def table_stat_month():
    dt_now = datetime.now()
    year_month = dt_now.strftime('%Y-%m')
    year = dt_now.strftime('%Y')
    month = dt_now.strftime('%m')
    if request.method == 'POST':
        year_month = request.form["month"]
        year = year_month.split('-')[0]
        month = year_month.split('-')[1]

    # stat 테이블 전체 조회해서 전체 직원 정보 추출
    result = []
    for row in select_stat_query_whole():
        # select_log_query_year_employee("연도", "이메일", "이름")
        list = select_log_query_year_month_employee(year_month, row['email'], row['name'])
        cnt_vacation = 0  # 연차 횟수
        cnt_half_vacation = 0  # 반차 횟수
        for element in list:
            # 결재까지 승인되면 stat 업데이트
            if element['confirmation'] == "승인":
                start_date = datetime.strptime(element['start_date'], "%Y-%m-%d")
                end_date = datetime.strptime(element['end_date'], "%Y-%m-%d")
                date_diff = end_date - start_date

                # 연차면 일수 차이만큼 횟수에 더하기 / 반차면 0.5만 더하기
                if element['type'] == "연차":
                    cnt_vacation += (date_diff.days + 1)
                else:
                    cnt_half_vacation += 0.5

        result.append([row['email'], row['name'], cnt_vacation, cnt_half_vacation])

    return render_template("table_stat_month.html", data=result, current_year=year, current_month=month)


# log 테이블에 휴가 신청에 대한 내역 추가
    insert_log_query(cliname, clitype, occur, action, charge, perform, day, comment)

if __name__ == '__main__':
    app.run(host="192.168.219.29", port="9730", debug=True)