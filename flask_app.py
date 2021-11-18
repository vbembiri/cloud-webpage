#Author- Vamshi B

import os
from flask import Flask,request,render_template

flask_app = Flask(__name__)

def tlparser(file, p):
    f = open(p+file)
    log = f.read()
    f.close()
    
    hrs = 0
    mins = 0
    log_lines = log.splitlines()
    
    for line in log_lines:
        if 'am' in line or 'pm' in line:
            flag = 0
            for i in range(len(line)):
                if flag > 2:
                    break
                if flag == 0 and (line[i:i+2]=='am' or line[i:i+2] == 'pm'):
                    st = line[i-5:i]
                    flag += 1
                elif flag == 1 and (line[i:i+2]=='am' or line[i:i+2] == 'pm'):
                    en = line[i-5:i]
                    flag += 1
                elif flag == 2:
                    m_st = int(st[-2:])
                    m_end = int(en[-2:])
                    h_st = int(st[:2].strip())
                    h_end = int(en[:2].strip())
                    
                    mi = 0
                    hr = 0
                    
                    if m_st > m_end:
                        mi = 60 - (m_st-m_end)
                        hr = hr - 1
                    else:
                        mi = m_end - m_st

                    if h_st > h_end:
                        hr = hr + (12 - (h_st - h_end))
                    else:
                        hr = hr + h_end - h_st
                    
                    hrs += hr
                    mins += mi
                    
                    flag = 0
                    break
            
    hrs += (mins//60)
    mins = (mins%60)
    return 'Time for {}:'.format(file)+str(hrs)+' hours '+ str(mins)+' minutes'

@flask_app.route("/")
def main():
    log_list = os.listdir("./log_files")
    return render_template('main.html',log_list=log_list)

@flask_app.route("/calculate",methods=["POST","GET"])
def calculate():
    fname = request.form.get("filename")
    log_list = os.listdir("./log_files")
    time = tlparser(fname,p='./log_files/')
    return render_template('main.html',log_list=log_list,time=time)

@flask_app.route("/upload",methods=["POST"])
def upload():
    log_list = os.listdir("./log_files")
    uploaded_file = request.files["uploadfile"]
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        time = tlparser(uploaded_file.filename, p=".\\")
    else:
        time = 'No file given'
    return render_template('main.html',log_list=log_list,time=time)

if __name__== "__main__":
    flask_app.run(debug = True)