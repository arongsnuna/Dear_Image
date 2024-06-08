from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return f'''<!doctype html>
    <html>
        <body>
            초기화면
        </body>
    </html>
    '''

@app.route('/start') #입력 받은 값 전송
def start():
    return f'''<!doctype html>
    <html>
        <body>
            시작화면
        </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
