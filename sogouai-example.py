# -*- coding: utf-8 -*-

'''
create by : joshua zou
create date : 2018.4.9
Purpose: check sougou ai api
'''

import glob,os
from SougouAPIMsg import *

#改成你自己搜狗AI的APPID、APPKEY、SecretKey
AppID = '0000'
ApiKey = '*********'
SecretKey= '0PLvS-AHShmq**************'

if __name__ == "__main__":
    sg = SougouAPIMsg(AppID,ApiKey,SecretKey)
    for file in glob.glob('D:\python\*.jpg'):
        filename=os.path.split(file)[1].split('.')[0]
        #调用ocr识别
        apiname = 'ocr'
        rest =sg.apiSougouOcr(apiname,file)
        #调用身份证识别
        #rest =sg.apiSougouOcr('idcard',file)
        

        js= rest.json()
        retext =""
        if apiname=='ocr':
            #文字识别，rest应答包，字符串
            #成功  {"result":[{"content":"01245177\n","frame":["0,0","207,0","207,59","0,59"]}],"success":1}
            #失败  {"success":0}            
            if js['success']==1 :
                retext = js['result'][0]['content'].strip()                 
        elif apiname == 'idcard':
            #身份证识别应答包，逼死强迫症啊，请求结构，应答结构都不一样
            '''
            {
            "result": {
            "住址": "xxxxxx",
            "公民身份号码": "11001xxx30",
            "出生": "19900101",
            "姓名": "xxXX",
            "性别": "X",
            "民族": "xxx"
            },
            "status": 0,
            "statusText": "Success"
            }
            '''
            if js['status']==0 :
                retext = js['result']['公民身份号码'].strip()            
        print(filename,retext)
