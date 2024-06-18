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