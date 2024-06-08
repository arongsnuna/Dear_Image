from flask import Flask, request, render_template, redirect, url_for, send_file
import os
import sys
from db_connection import connect_to_database
import uuid

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

if __name__ == '__main__':
    app.run(debug=True)
