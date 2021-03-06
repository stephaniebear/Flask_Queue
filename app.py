from flask import Flask, render_template, request, redirect, url_for
from flask import send_file #For download file
import threading
import os

app = Flask(__name__)

def thread_callback():
    app.config.from_pyfile("main.py", silent=True)

@app.route('/')
def index():
    # Read logs
    path = os.path.dirname(os.path.realpath(__file__))
    path += '/logs'

    logs_file_dicts = {} #Dictionary
    logs_file_name = []
    temp_logs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            if file == 'date.txt':
                print('Skip date file')
            else:
                print('File : ' + str(os.path.join(file))) # Read logs files
                f = open('logs/' + str(os.path.join(file)), 'r')
                logs_file_name.append(str(os.path.join(file)).replace(".txt","")) # Collect file name
                for row in f:
                    if len(row) > 1:
                        temp_logs = row.strip().split(',')
                        logs_file_dicts.update({temp_logs[1]:temp_logs[0]})
                f.close()

    return render_template('index.html', logs_file_dicts=logs_file_dicts, logs_file_name=logs_file_name)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        messages = []
        if request.form['dol_admin_password'] != "manage_ch2":
            print('Admin password incorrect !!')
            messages.append('Incorrect your password')
            dol_office = open('configs/dol_office.txt', 'r', encoding="UTF-8") # 
            return render_template('configs.html', messages=messages, dol_office=dol_office)
        # f = open('configs/config.txt', 'r')
        # for row in f:
        #     tempContent = row.replace('\n', ' ')
        #     content.append(tempContent.decode('unicode-escape'))
        #     #tempContent.decode('unicode-escape')
        #     #print('Content in file : ' + tempContent.decode('unicode-escape'))
        # f.close()

        #Get Office
        dol_office = request.form['dol_office']
        dol_office = dol_office.encode('ascii', 'backslashreplace')
        dol_office = str(dol_office).replace(" "," \n")
        dol_office = str(dol_office).replace("\\\\","\\")
        dol_office = str(dol_office).replace("b'","")
        dol_office = str(dol_office).replace("'","")
        
        #dol_office = str(dol_office).replace("\\r","")
        print(dol_office)

        # Save to config.txt
        f = open('configs/config.txt', 'w')
        f.write(dol_office)
        f.close()

        # Get Telephone number
        dol_telephone = request.form['dol_telephone_number']
        print(dol_telephone)
        f = open('configs/tel.txt', 'w')
        f.write(dol_telephone)
        f.close()

        # Get QR Code
        uploaded_file = request.files['dol_qrcode']
        if uploaded_file.filename != '':
            uploaded_file.filename = 'configs/qrcode.png' # Rename files
            print(uploaded_file.filename)
            uploaded_file.save(uploaded_file.filename)
    else:
        print('Method : GET')
    return redirect(url_for('index'))

@app.route('/configs')
def configs():
    # Read logs
    path = os.path.dirname(os.path.realpath(__file__))
    path += '/logs'

    logs_file_dicts = {} #Dictionary
    temp_logs = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            if file == 'date.txt':
                print('Skip date file')
            else:
                print('File : ' + str(os.path.join(file))) # Read logs files
                f = open('logs/' + str(os.path.join(file)), 'r') # 
                for row in f:
                    if len(row) > 1:
                        temp_logs = row.strip().split(',')
                        logs_file_dicts.update({temp_logs[1]:temp_logs[0]})
                f.close()

    # for (key, value) in logs_file_dicts.items():
    #     print('Queue : ' + key + ' Timestamp : ' + value)

    # Get Dol office
    
    dol_office = open('configs/dol_office.txt', 'r', encoding="UTF-8") # 

    print(type(dol_office))

    return render_template('configs.html', logs_file_dicts=logs_file_dicts, dol_office=dol_office)

@app.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == "POST":
        print('-------- view -------------')
        print(request.form['viewDate'])

        print(request.form['inlineRadioOptions'])

        if request.form['inlineRadioOptions'] == "option1":
            # Read logs
            path = os.path.dirname(os.path.realpath(__file__))
            path += '/logs'

            logs_file_dicts = {} #Dictionary
            logs_file_name = []
            temp_logs = []

            f = open('logs/' + str(request.form['viewDate']) + '.txt', 'r')
            for row in f:
                if len(row) > 1:
                    temp_logs = row.strip().split(',')
                    logs_file_dicts.update({temp_logs[1]:temp_logs[0]})
            f.close()

            for file in os.listdir(path):
                if file.endswith(".txt"):
                    if file == 'date.txt':
                        print('Skip date file')
                    else:
                        logs_file_name.append(str(os.path.join(file)).replace(".txt","")) # Collect file name
            return render_template('index.html', logs_file_dicts=logs_file_dicts, logs_file_name=logs_file_name)
        elif request.form['inlineRadioOptions'] == "option2":
            path = 'logs/' + str(request.form['viewDate']) + '.txt'
            return send_file(path, as_attachment=True)
        else:
            path = 'logs/' + str(request.form['viewDate']) + '.txt'

            print('Delete')
            os.remove(path)
            return redirect(url_for('index'))

    return render_template('index.html', logs_file_dicts=logs_file_dicts, logs_file_name=logs_file_name)

@app.route('/run_script')
def run_script():

    #app.config.from_pyfile("main.py", silent=True)
    thr = threading.Thread(target=thread_callback)
    thr.start()

    print('Start Threading')
    return render_template('index.html')

@app.route('/stop_script')
def stop_script():

    print('Start Threading')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)