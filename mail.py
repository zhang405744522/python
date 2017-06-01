 #coding: utf-8

import os
import sys
import time
import datetime
import re
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

_mail_host = '10.26.7.16' 
_user = 'weixue02@baidu.com'  
        
def sendEmail(_mailto, _mailcc, subject, message, attachFileList=[]):
    mail = constructEmail(_mailto, _mailcc, subject, message, attachFileList)
    try: 
        mailtoList = _mailto.split(',')
        for mailto in mailtoList:
            smtpServer = smtplib.SMTP(host=_mail_host, port=25)
            smtpServer.sendmail(_user, mailto, mail.as_string())
            smtpServer.close()
        # After sending the dmp file to tester, delete them.
        for file in attachFileList:
            os.remove(file)
    except Exception as e:
        print('Exception got when sending email.')
    
def constructEmail(_mailto, _mailcc, subject, message, attachFileList):
    msg = MIMEMultipart()
    for attachFile in attachFileList:
        if attachFile != None and attachFile != '':             
            att = MIMEText(open(attachFile, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att["Content-Disposition"] = 'attachment;filename="%s"'% os.path.split(attachFile)[1]
            msg.attach(att)
    
    body = MIMEText(message, 'html', _charset='utf-8')
    msg.attach(body)
    msg['To'] = _mailto
    msg['cc'] = _mailcc
    msg['from'] = _user
    msg['subject'] = subject
    return msg

def uuap_login_pre(url):
    req_params = {}
    try:
        response = requests.get(url)
        # match lt
        pattern1 = re.compile(r'name="lt"\svalue="(.*?)"')
        match1 = pattern1.search(response.text)       
        if match1:      
            req_params['lt'] = match1.group(1)
        else:
            print ('*' * 50)
            print ('error when match lt')

        # match execution
        pattern2 = re.compile(r'name="execution"\svalue="(.*?)"')
        matche2 = pattern2.search(response.text)
        if matche2:
            req_params['execution'] = matche2.group(1)
        else:
            print ('*' * 50)
            print ('error when match execution')

        # match jessionid
        pattern3 = re.compile(r'jsessionid=(.*?)\"')
        matche3 = pattern3.search(response.text)
        if matche3:
            req_params['jsessionid'] = matche3.group(1)
        else:
            print ('*' * 50)
            print ('error when match jsessionid')
        return req_params      
    except Exception as e:
        print ('Exception: %s' % str(e))

def uuap_login(url, user_name, password):
    params = {}
    ret_params = uuap_login_pre(url)  
    params['username'] = user_name
    params['password'] = password
    params['remeberMe'] = "on"
    params['_eventId'] = "submit"
    params['type'] = "1"
    params['lt'] = ret_params['lt']
    params['execution'] = ret_params['execution']
    cookies =  {    
                 'JSESSIONID': ret_params['jsessionid']
               }
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded', 
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
              }
    s = requests.Session()
    r = s.post(url, data=params, headers=headers, cookies=cookies)
    str_url = url + '?service=http://sh.ci.iyuntian.com/securityRealm/finishLogin'
    cookies['UUAPTGC'] = r.cookies['UUAPTGC']  
    r2 = s.post(str_url, cookies=cookies)
    return s

def get_user(param_url):
    jennkins_request = uuap_login('https://uuap.baidu.com/login',r'buildbot',r'Gt#5rxRV7B2!@#')
    r = jennkins_request.get(param_url)
    print (url)
    print (type(r.text))
    if r.text.find('Started by timer') != -1:
        print ('Started by timer')
        name = 'timer'
    else:
        textlist = r.text.split(' ')
        name = textlist[3].split('\r\n')[0]
        print (name)
    return name, r.text

if __name__ == '__main__':
    if(len(sys.argv)!=3):
        print ('param invalid')
    url = sys.argv[1]+ sys.argv[2]+'/consoleText'
    try:
        if os.system('UV4_build.bat')!=0:
           raise Exception()
        print '编译成功'
    except:
        name, msg = get_user(url)
        msgs = msg.replace('\n','<br>')
        if name != 'timer':
            mailto = name + '@baidu.com'
        else:
            mailto = 'zhangguohua02@baidu.com,zhouhua01@baidu.com,panhaijun@baidu.com,suhao@baidu.com,duanlian01@baidu.com,weixue02@baidu.com'
        subject = '【Iot 编译失败】'
        message = '详细信息请查看: <br> &nbsp;&nbsp %s%s <br> <br> %s'%(sys.argv[1],sys.argv[2],msgs)
        message.decode('utf-8').encode('gb18030') 
        sendEmail(mailto, '', subject, message)
        raise Exception('Iot 编译失败')
            
    