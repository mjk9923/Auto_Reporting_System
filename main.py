import csv

from flask import *
from mysql import *
# import smtplib
# from email.mime.text import MIMEText
# import pandas as pd
#import numpy as np

app = Flask(__name__)

#@app.route('/chanwoojjangjjangman')
#def chanwoojjangjjangman():
#    return render_template('client_com_request.html')


# 고객사 등록 페이지 라우팅
@app.route('/client_com_request')
def client_com_request():
    return render_template('client_com_request.html')

@app.route('/shot_complet')
def shot_complet():
    return render_template('shot_complet.html')

# 등록 버튼 클릭 시
@app.route('/client_com_request_click', methods=["GET", "POST"])
def client_com_request_click():
    cliname = request.form.get("cliname", type=str)
    clitype = request.form.get("pointCheck", type=str)
    

    # 만약 테이블에 해당 고객사에 대한 데이터가 존재하지 않는다면 추가
    if not exist_employee(cliname, clitype):
        insert_worklist_query(cliname, clitype)

    return render_template("client_com_pop.html")


# 등록 내역 조회
@app.route("/date_log", methods=["POST", "GET"])
def date_log():
    dt_now = datetime.now()
    year_month = dt_now.strftime('%Y-%m')
    year = dt_now.strftime('%Y')
    month = dt_now.strftime('%m')
    filter_type = "전체"
    if request.method == 'POST':
        year_month = request.form["month"]
        filter_type = request.form["filter_type"]
        year = year_month.split('-')[0]
        month = year_month.split('-')[1]

    # select_log_query_date("원하는 연월(YYYY-MM)")
    result = select_log_query_month(year_month)

    # CSV 파일로 만들기
    #vacation_log_csv = open('C:/temp/vacation_log.csv', 'w', newline='')
    vacation_log_csv = open('/tmp/vacation_log.csv','w', encoding = 'utf-8', newline='')
    vacation_log_csv_wr = csv.writer(vacation_log_csv)
    vacation_log_csv_wr.writerow(
        ['이메일', '이름', '휴가 종류', '시작 날짜', '종료 날짜', '연차 사용 횟수', '사유', '결재 상태', '코멘트'])

    # 종료 날짜 - 시작 날짜 계산 후 컬럼 추가
    date_diff_list = []
    for element in result:
        start_date = datetime.strptime(element['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(element['end_date'], "%Y-%m-%d")
        date_diff = end_date - start_date

        if element['type'] == "연차":
            date_diff_list.append(date_diff.days + 1)
        else:
            date_diff_list.append(0.5)

        vacation_log_csv_wr.writerow(
            [element['email'], element['name'], element['type'], element['start_date'], element['end_date'],
             date_diff.days + 1, element['reason'], element['confirmation'], element['comment']])

    # CSV 닫기
    vacation_log_csv.close()

    # log 테이블에서 휴가 신청페이지서 선택한 내역 삭제
    # delete_log_query("id")

    return render_template("vacation_log.html", data=result, current_year=year, current_month=month,
                           date_diff_list=date_diff_list, filter_type=filter_type)



# log 테이블에 휴가 신청에 대한 내역 추가
    insert_log_query(cliname, clitype, occur, action, charge, perform, day, comment)

if __name__ == '__main__':
    app.run(host="192.168.219.29", port="5556", debug=True)