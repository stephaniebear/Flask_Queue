from flask import Flask, render_template, request, redirect, url_for
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

    return render_template('index.html', logs_file_dicts=logs_file_dicts, dol_office=dol_office)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    def getThaiCharacter(character):
        switcher = {
            'ก' : '\u0E01',
            'ข' : '\u0E02',
            'ฃ' : '\u0E03',
            'ค' : '\u0E04',
            'ฅ' : '\u0E05',
            'ฆ' : '\u0E06',
            'ง' : '\u0E07',
            'จ' : '\u0E08',
            'ฉ' : '\u0E09',
            'ช' : '\u0E0A',
            'ซ' : '\u0E0B',
            'ฌ' : '\u0E0C',
            'ญ' : '\u0E0D',
            'ฎ' : '\u0E0E',
            'ฏ' : '\u0E0F',
            'ฐ' : '\u0E10',
            'ฑ' : '\u0E11',
            'ฒ' : '\u0E12',
            'ณ' : '\u0E13',
            'ด' : '\u0E14',
            'ต' : '\u0E15',
            'ถ' : '\u0E16',
            'ท' : '\u0E17',
            'ธ' : '\u0E18',
            'น' : '\u0E19',
            'บ' : '\u0E1A',
            'ป' : '\u0E1B',
            'ผ' : '\u0E1C',
            'ฝ' : '\u0E1D',
            'พ' : '\u0E1E',
            'ฟ' : '\u0E1F',
            'ภ' : '\u0E20',
            'ม' : '\u0E21',
            'ย' : '\u0E22',
            'ร' : '\u0E23',
            'ฤ' : '\u0E24',
            'ล' : '\u0E25',
            'ฦ' : '\u0E26',
            'ว' : '\u0E27',
            'ศ' : '\u0E28',
            'ษ' : '\u0E29',
            'ส' : '\u0E2A',
            'ห' : '\u0E2B',
            'ฬ' : '\u0E2C',
            'อ' : '\u0E2D',
            'ฮ' : '\u0E2E'
        }
        return switcher.get(character, "Error")

    if request.method == 'POST':
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
        dol_office = str(dol_office).replace(" ","\n")
        dol_office = str(dol_office).replace("\\\\","\\")
        dol_office = str(dol_office).replace("b'","")
        dol_office = str(dol_office).replace("'","")
        
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
    app.run(debug=True, host='127.0.0.1', port=5000)
