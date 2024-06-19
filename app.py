from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import sys
from db_connection import connect_to_database
import uuid
from flask import Flask, request, redirect, url_for
import os
import boto3
import uploads_utils
from werkzeug.utils import secure_filename
import uuid

module_path = os.path.abspath(os.path.join('..'))
inputs = {}

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
    # if(session_id is not None):
    #     delete_query = "DELETE FROM sessions WHERE session_id = %s"
    #     cursor.execute(delete_query, (session_id,))
    #     conn.commit()
    #     session_id = None
    conn = connect_to_database()
    cursor = conn.cursor(buffered=True)
    session_id = str(uuid.uuid4())
    insert_query = "INSERT INTO session (session_id) VALUES (%s)"
    cursor.execute(insert_query, (session_id,))
    conn.commit()

    return f'''<!doctype html>
    <html>
        <body>
            시작화면
        </body>
    </html>
    '''
@app.route('/imgupload')
def imgupload():
    return f'''<!doctype html>
    <html>
        <body>
            <form action="http://localhost:5000/command_image"
                method="POST"
                enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" />
            </form>
        </body>
    </html>
    '''

@app.route('/command_image', methods=['POST'])
def imgUploader():
    session_id =  str(uuid.uuid4())

    s3 = uploads_utils.s3Connection()
    bucket = 'dear-image-flask'
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if uploads_utils.allowedFile(file.filename):
        filename = secure_filename(file.filename)

        s3_filepath = f'{session_id}/{filename}'
        s3.upload_fileobj(file, bucket, s3_filepath)

    # 리다이렉션 어디로 해야할지..
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">File uploaded successfully</a></h1>
        </body>
    </html>
    '''

@app.route('/command')
def command():
    return f'''<!doctype html>
    <html>
        <body>
            <form action="/nextpage" method="post">
                <label for="command_contents">명령을 입력해주세요</label><br>
                <input type="text" id="command_contents" name="command_contents"><br><br>
                <input type="submit" value="입력">
            </form>
        </body>
    </html>
    '''

@app.route('/nextpage', methods=['POST']) #입력 받은 값 전송
def nextpage():
    command_contents = request.form['command_contents']
    conn = connect_to_database()
    cursor = conn.cursor(buffered=True)
    session_id = str(uuid.uuid4())
    insert_command_query = "INSERT INTO commands (session_id, command_contents) VALUES (%s, %s)"
    cursor.execute(insert_command_query, (session_id, command_contents))
    conn.commit()

    inputs['command_contents'] = command_contents
    return redirect(url_for('command_image'))


app.run()
if __name__ == '__main__':
    app.run(debug=True)
