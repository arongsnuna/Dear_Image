# 서버 구동
from flask import Flask, Response, request, render_template, redirect, url_for, send_file
from flask_cors import CORS
import requests
from visprog_module import imageHandler
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from PIL import Image
from IPython.core.display import HTML
from functools import partial
from engine.utils import ProgramGenerator, ProgramInterpreter
from prompts.imgeEdit import PROMPT
import googletrans
from dotenv import load_dotenv
load_dotenv()

#DB
from db_connection import connect_to_database
import uuid
import uploads_utils
from werkzeug.utils import secure_filename


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

interpreter = ProgramInterpreter(dataset='imageEdit')
def create_prompt(instruction):
    return PROMPT.format(instruction=instruction)

generator = ProgramGenerator(prompter=create_prompt)


session_id = None
conn = connect_to_database()
cursor = conn.cursor(buffered=True)


inputs = {}
origin = 'result/original.png'
translator = googletrans.Translator()

@app.route('/')
def index():
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">visprog</a></h1>
            <div>초기화면<div>
            <ol>
                <a href="/start">들어가기</a>
            </ol>
        </body>
    </html>
    '''

@app.route('/start') #입력 받은 값 전송
def start():
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">visprog </a></h1>
            <div>시작화면<div>
            <ol>
                <a href="/imgupload">들어가기</a>
            </ol>
        </body>
    </html>
    '''

@app.route('/imgupload') #사진 업로드
def imgupload():
    global session_id
    # 기존 세션이 있으면 삭제
    if session_id:
        # 세션과 관련된 모든 데이터를 삭제
        sql_delete_images = 'DELETE FROM OriginalImage WHERE session_id=%s'
        cursor.execute(sql_delete_images, (session_id,))
        conn.commit()

        sql_delete_session = 'DELETE FROM Session WHERE session_id=%s'
        cursor.execute(sql_delete_session, (session_id,))
        conn.commit()

    # 새로운 세션 생성
    session_id = str(uuid.uuid4())
    sql_insert = 'INSERT INTO Session (session_id) VALUES (%s)'
    cursor.execute(sql_insert, (session_id,))
    conn.commit()
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">visprog </a></h1>
            <form action="http://localhost:5000/command_image"
                method="POST"
                enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        </body>
    </html>
    '''

#이미지 저장 및 커맨드 입력
@app.route('/command_image', methods=['POST'])
def imgUploader():
    s3 = uploads_utils.s3Connection()
    bucket = 'dear-image-flask'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if uploads_utils.allowedFile(file.filename):
        filename = secure_filename(file.filename)

        s3_filepath = f'{session_id}/{filename}'
        s3.upload_fileobj(file, bucket, s3_filepath)

    location = s3.get_bucket_location(Bucket=bucket)["LocationConstraint"]
    url = f"https://{bucket}.s3.{location}.amazonaws.com/{s3_filepath}"
    sql = 'INSERT INTO OriginalImage (filepath, session_id) VALUES (%s, %s)'
    val = (url, session_id)
    cursor.execute(sql, val)
    conn.commit()

    return f'''<!doctype html>
    <html>
        <body>
            <form action="/imageEdit" method="post">
                <label for="command_contents">명령을 입력해주세요</label><br>
                <input type="text" id="command_contents" name="command_contents"><br><br>
                <input type="submit" value="입력">
            </form>
        </body>
    </html>
    '''


#입력 받은 값 전송
@app.route('/imageEdit', methods=['POST'])
def imageEdit():
    data = request.json
    command_contents = data.get('command_contents')
    # 커맨드 로그
    print(f'command_contents: {command_contents}') 
    en_command = translator.translate(command_contents, dest='en')
    # 영어 번역 로그(visprog_module.imageHandler의 특정 커맨드 추가)
    print(f'en_command: {en_command}')
    sql1 = 'SELECT filepath FROM OriginalImage WHERE session_id=%s'
    val1 = (session_id,)
    cursor.execute(sql1, val1)
    image_path = cursor.fetchone()[0]

    # 커맨드에 특정 문자가 없으면 chatgpt, 있으면 이미지 수정
    result = imageHandler(image_path, en_command.text, interpreter, generator)
    # 결과 값 확인
    if isinstance(result, str):
        # 결과 값이 텍스트일 경우
        return {'type': 'text', 'message': result}
    else:
        # 결과 값이 이미지일 경우
        unique_filename = f'edited_{uuid.uuid4().hex}.png'
        result_path = os.path.join('result', unique_filename)
        result.save(result_path)

        s3 = uploads_utils.s3Connection()
        bucket = 'dear-image-flask'
        s3_filepath = f'{session_id}/{unique_filename}'
        s3.upload_file(result_path, bucket, s3_filepath)

        location = s3.get_bucket_location(Bucket=bucket)["LocationConstraint"]
        url = f"https://{bucket}.s3.{location}.amazonaws.com/{s3_filepath}"

        sql2 = 'UPDATE OriginalImage SET filepath=%s WHERE session_id=%s'
        val2 = (url, session_id)
        cursor.execute(sql2, val2)
        conn.commit()

        return {'type': 'image', 'url': url}

@app.route('/get_image')
def get_image():
    url = request.args.get('url')
    if not url:
        return 'No URL provided', 400
    response = requests.get(url)

    if response.status_code == 200:
        return Response(response.content, mimetype='image/png')
    else:
        return 'Image not found', 404
app.run()
