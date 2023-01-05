from flask import Flask
from flask import render_template

# 터미널에서 nohup python -u .py & 실행 


### Flask를 통해 사용자에게 웹 어플리케이션 제공 ###
app = Flask(__name__)


# 현재 주차장의 상태를 park_state.txt를 불러와
# render_template를 사용하여 html(index.html)로 넘겨줌
park = ['False', 'False']

@app.route('/')
def main():
    f = open('/home/seungjo/project/park_state.txt', 'r')
    line = f.readline()
    park = line.split(',')
    return render_template('index.html', park = park)

@app.route('/index.html')
def index():
    f = open('/home/seungjo/project/park_state.txt', 'r')
    line = f.readline()
    park = line.split(',')
    return render_template('index.html', park = park)

@app.route('/cam.html')
def cam():
    return render_template('cam.html')


app.run(host = "0.0.0.0", port = "5005", debug = True, threaded = True)
