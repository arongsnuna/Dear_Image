from flask import Flask, request, render_template, redirect, url_for, send_file
#from gqa_module import *
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
#%env OPENAI_API_KEY=
from PIL import Image
from IPython.core.display import HTML
from functools import partial
from engine.utils import ProgramGenerator, ProgramInterpreter
from prompts.gqa import create_prompt
#import googletrans

#translator = googletrans.Translator()

app = Flask(__name__)
interpreter = ProgramInterpreter(dataset='gqa')
prompter = partial(create_prompt,method='all')
generator = ProgramGenerator(prompter=prompter)

# 전역 변수를 사용하여 입력값을 저장할 딕셔너리 선언
inputs = {}

@app.route('/')
def index():
    return f'''<!doctype html>
    <html>
        <body>
            <form action="/nextpage" method="post">
                <label for="name">찾을 대상을 입력해주세요:</label><br>
                <input type="text" id="name" name="name"><br><br>
                <input type="submit" value="찾기">
            </form>
        </body>
    </html>
    '''

@app.route('/nextpage', methods=['POST']) #입력 받은 값 전송
def nextpage():
    name = request.form['name']
    inputs['name'] = name
    return redirect(url_for('find_object'))

@app.route('/find_object')
def find_object():
    # 저장된 입력값을 가져와서 출력
    url = 'assets/camel1.png'
    name = inputs.get('name', None)
    chat = 'find'+name
    result = exe_gqa(url, chat, interpreter, prompter, generator)
    en_name = translator.translate(name, dest='en')
    result_path = 'result/'+en_name.text+'.jpg' #결과 이미지 경로

    if os.path.exists(result_path): #result 폴더에 파일이 존재할 경우
        return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">visprog</a></h1>
            <h2>찾은 대상: {name}</h2>
            <hr><img src='/get_image?url={result_path}'></hr>
        </body>
    </html>
    '''
    else:
        return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">visprog</a></h1>
            <h2>대상을 찾을 수 없습니다.</h2>
        </body>
    </html>
    '''
    
@app.route('/get_image')
def get_image():
    # URL로 전달된 파일 경로 가져오기
    url = request.args.get('url')
    
    # 파일 경로로부터 이미지 파일 읽어오기
    img_path = os.path.join(app.root_path, url)
    
    # 이미지 파일을 클라이언트에게 전송
    return send_file(img_path)


app.run()
