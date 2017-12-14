#-*- coding: utf-8-*-
from flask import Flask, render_template, request, url_for, redirect, make_response
import MySQLdb
from datetime import datetime

app = Flask(__name__)

# 데이터베이스에 연결하는 방법. 비밀번호 및 DB는 사용자 정의에 따라 변경하시면 됩니다.
def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="dbsdud12", db="Origin_Server")
    c = conn.cursor()
    return c, conn

# 뭔가 잘못되었을 때 에러메세지를 띄울 수 있도록 하는 함수.. message 변수를 전달하여 출력되는 에러메세지를 변경할 수 있음.
@app.route('/error')
def error():
    return render_template('error.html')

per_page = 15 # 한페이지에 표시되는 정보는 15개.. 아직 구현되지 않은 부분


# 메인페이지를 렌더링해주는 함수. 페이지네이션을 통해서 땃땃땃/1 이런식으로 해보려고 했으나, 아직 구현안된 부분입니다.
@app.route('/', defaults={'page' : 1})
@app.route('/<int:page>')
def homepage(page):
    # try:
    c, conn = connection() # DB에 연결하고
    c.execute("SELECT * FROM config")
    data = c.fetchall() # mysql에서 실행하면 뜨는 정보를 리스트의 형태로 가져오는 모듈
    templist = []
    for element in data: # 이중리스트를 전달할 수 없기 때문에, 반복문을 통해서 푼 다음 넘깁니다.
        templist.append(list(element))
    c.execute("SELECT COUNT(*) FROM config")
    articles = c.fetchone()[0]
    pageno = articles//per_page + 1 # 한페이지에 15개씩 표시할려면 총 페이지가 몇개인지 계산하는 부분. 총 글이 50개인데 1페이지당 15개면, 50//15는 3이니 페이지는 총 3+1개가 필요
    conn.commit() # 꼭 필요한 부분. 커밋하고 세션 종료해줘야 반영이 됩니다.
    conn.close()
    return render_template('homepage.html', row = templist, article = articles, number = pageno, page=page) # 필요한 변수를 html파일로 넘길 수 있습니다.

    # except Exception as e:
    #     return render_template("error.html")

# New버튼을 눌러 설정한 Response값 DB에 저장
@app.route('/make_new_config', methods=['POST'])
def make_new_config():
    # Configuration Name
    if request.form['configuration_name']:
        configuration_name = request.form['configuration_name']

    # Path Name
    if request.form['path_name']:
        path_name = request.form['path_name']

    # Response Code
    if request.form['response_code']:
        response_code = request.form['response_code']

    # Content Type
    if request.form['content_type']:
        content_type = request.form['content_type']
    else:
        content_type = 'text/html; charset=utf-8'

    # Content Length
    if request.form['content_length']:
        content_length = request.form['content_length']
    else:
        content_length = None

    # Content Encoding
    if request.form['content_encoding']:
        content_encoding = request.form['content_encoding']
    else:
        content_encoding = None

    # Transfer Encoding
    if request.form['transfer_encoding']:
        transfer_encoding = request.form['transfer_encoding']
    else:
        transfer_encoding = None

    # Custom Response Header
    if request.form['rc_header']:
        rc_header = request.form['rc_header']
    else:
        rc_header = None

    # Body(Text)
    if request.form['textarea']:
        body = request.form['textarea']
    else:
        body = None

    # Body(File)
    file = request.files['file[]'].read()
    if str(file):
        body = file

    # DB에 Insert 하는 부분
    c, conn = connection()
    c.execute("SELECT COUNT(*) FROM config")
    count = c.fetchone()[0]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO config VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (int(count)+1, configuration_name, path_name, response_code, content_type, content_length, content_encoding, transfer_encoding, rc_header, time, body))

    conn.commit()
    conn.close()

    return redirect(url_for('homepage'))

# 수정 버튼 클릭 시 실행
@app.route('/editconfig_'+'<path>', methods=['GET', 'POST'])
def editconfig(path):
    # Configuration Name
    if request.form['configuration_name_edit']:
        configuration_name = request.form['configuration_name_edit']

    # Path Name
    if request.form['path_name_edit']:
        path_name = request.form['path_name_edit']

    # Response Code
    if request.form['response_code_edit']:
        response_code = request.form['response_code_edit']

    # Content-Type
    if request.form['content_type_edit']:
        content_type = request.form['content_type_edit']
    else:
        content_type = None

    # Content-Length
    if request.form['content_length_edit']:
        content_length = request.form['content_length_edit']
    else:
        content_length = None

    # Content-Encoding
    if request.form['content_encoding_edit']:
        content_encoding = request.form['content_encoding_edit']
    else:
        content_encoding = None

    # Transfer Encoding
    if request.form['transfer_encoding_edit']:
        transfer_encoding = request.form['transfer_encoding_edit']
    else:
        transfer_encoding = None

    # Custom Header
    if request.form['rc_header_edit']:
        rc_header = request.form['rc_header_edit']
    else:
        rc_header = None

    # Body(Text)
    if request.form['te']:
        body = request.form['te']
    else:
        body = None

    # Body(File)
    file = request.files['file[]'].read()
    if str(file):
        body = file

    c, conn = connection()
    c.execute("SELECT * FROM config")
    count = c.fetchone()[0]

    # DB에 Update 하는 부분
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE config SET seq = %s, \
                             config_name = %s, \
                             path_name = %s, \
                             resp_code = %s, \
                             content_type = %s, \
                             content_length = %s, \
                             content_encoding = %s, \
                             transfer_encoding = %s, \
                             custom_header = %s, \
                             dates = %s \
                             body = %s \
               WHERE path_name = %s", (count, configuration_name, path_name, response_code, content_type, content_length, content_encoding, transfer_encoding, rc_header, time, body, path))

    conn.commit()
    conn.close()
    return redirect(url_for('homepage'))

# 설정 항목을 삭제할 때, DB에 저장된 로그까지 다 지우게 하는 함수
@app.route('/delconfig_'+'<path>', methods=['POST'])
def delconfig(path):
    c, conn = connection()
    c.execute("DELETE FROM config WHERE path_name = %s", (path)) # config 테이블에서 실제 설정값도 지우지만
    c.execute("DELETE FROM request_header WHERE path = %s", (path)) # request 테이블에서 관련 로그 기록도 다 지우도록
    conn.commit()
    conn.close()
    return redirect(url_for('homepage')) # 완료되면 리로딩 한번

# 모니터링을 하는 화면인데, 마찬가지로 페이지네이션 구현은 아직..
@app.route('/monitoring_'+'<path>', defaults={'page' : 1})
@app.route('/monitoring_'+'<path>'+'/<int:page>', methods=['GET','POST'])
def monitoring(path, page):

    c, conn = connection()
    request_header = {"Method" : "", 
                    "Accept" : "", 
                    "Accept-Encoding" : "",
                    "Accept-Language" : "",
                    "Cache-Control" : "",
                    "User-Agent" : "",
                    "Cookie" : "",
                    "Connection" : "",
                    "Host" : "",
                    "Custom-Headers" : "" }

    req = request.headers # 파이썬 모듈로 리퀘스트 헤더 정보 불러오고
    for element in req: # 키값으로 비교하고 찾아서 딕셔너리로 저장
        if(element[0] in request_header.keys()):
            request_header[element[0]] = element[1]
        else:
            request_header["Custom-Headers"] += element[1] +", " # 찾지 못한 부분은 일단 다 커스텀 헤더로 전달했으나, 추가 사항 필요

    print(request_header)
    c.execute("SELECT COUNT(*) FROM request_header")
    count = c.fetchone()[0]
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 노가다 작업으로 싹 디비에 넣어주는 과정
    c.execute("INSERT INTO request_header VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", \
                                                (count+1, request_header["Method"], path, request_header["Accept"], request_header["Accept-Encoding"], \
                                                request_header["Accept-Language"], request_header["Cache-Control"], request_header["User-Agent"], request_header["Cookie"], \
                                                request_header["Host"], request_header["Connection"], time, request_header["Custom-Headers"])) 
    conn.commit()
    conn.close()

    c, conn = connection()

    c.execute("SELECT COUNT(*) FROM request_header WHERE path = %s", (path))
    articles = c.fetchone()[0]
    pageno = articles//per_page + 1  # 페이지네이션을 위한 총 페이지 개수 몇개가 필요한지 계산..

    c.execute("SELECT * FROM request_header WHERE path = %s", (path))
    request_result = c.fetchall()

    c.execute("SELECT * FROM config WHERE path_name = %s", (path))
    response_result = c.fetchone()
    conn.commit()
    conn.close()
    
    return render_template("monitoring.html", resp = response_result, req = request_result, path = path, article = articles, number = pageno)


# Path name 입력 시 실행
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def path_test(path):
    # URL에 입력한 Path Name과 DB에 저장된 Path Name 비교
    # Path Name이 같은 DB정보를 불러온다
    c, conn = connection()
    c.execute("SELECT * FROM config WHERE path_name = %s",(path))
    result = c.fetchall()[0]
    conn.commit()
    conn.close()

    #######################################
    # result[0] : Sequence                #
    # result[1] : Configuration Name      #
    # result[2] : Path Name               #
    # result[3] : Response Code           #
    # result[4] : Content-Type            #
    # result[5] : Content-Length          #
    # result[6] : Content-Encoding        #
    # result[7] : Transfer-Encoding       #
    # result[8] : Custom Header           #
    # result[9] : Date                    #
    # result[10] : Response Body          #
    #######################################

    ch1 = None
    if result[8]:
        target = result[8]
        ch1 = target.splitlines()

    r = make_response(result[10])

    if ch1:
        for headers in ch1:
            ch1_split = headers.split(":")
            ch1_header = ch1_split[0]
            ch1_data = ch1_split[1].strip()
            r.headers[ch1_header] = ch1_data

    r.status_code = int(result[3])
    r.headers['Content-type'] = result[4]
    r.headers['Content-Length'] = int(result[5])

    if result[6]:
        r.headers['Content-Encoding'] = result[6]

    return r

if __name__ == "__main__":
    app.run()
