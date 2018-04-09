# -*- coding: utf-8 -*-

'''
create by : joshua zou
create date : 2018.4.9
Purpose: check sougou ai api
'''

import requests
import base64
import hashlib
import hmac
import time
from urllib import parse
import json
from SougouAPI import *

class SougouAPIMsg(object):
    def __init__(self,AppID=None,ApiKey=None,SecretKey=None):
        if not AppID: AppID = '88888'
        if not ApiKey: ApiKey = '5ADwS88888888Dtr6QG2'
        if not SecretKey: SecretKey= '0PLvS-AH8888888889n6NF6fVVTt7m'
        self.__app_id= AppID 
        self.__app_key= ApiKey 
        self.__app_secret= SecretKey 

    
    def get_time_stamp(self):
        return str(int(time.time()))
    
    '''
    1、应用相关前缀 {AuthPrefix}
    {AuthPrefix}=sac-auth-v1/{accessKey}/{secondsSinceEpoch}/{expirationPeriodInSeconds}
    2、请求相关数据 {Data}        
    {Data}={REQUEST_METHOD} + "\n" + {HOST} + "\n" + {URI} + "\n" + {SORTED_QUERY_STRING}
    其中，REQUEST_METHOD 为请求使用的 HTTP 方法, 如: GET|POST|PUT|DELETE
    HOST 为服务使用的域名, 如: api.ai.sogou.com
    URI 为请求的服务路径, 如: /speech/asr
    SORTED_QUERY_STRING 把 URL 中的 Query String（即 URL 中 “?” 后面的 “k1=v1&k2=v2” 字符串）进行编码后的结果。        
    编码方法为：
    将 Query String 根据 & 拆开成若干项，对每一项转换为 UriEncode(key) + "=" + UriEncode(value) 的形式, 其中 value 可以是空字符串
    将上面转换后的所有字符串按照字典顺序排序。
    将排序后的字符串按顺序用 & 符号链接起来。
    3、生成签名 {Signature}        
     {Signature}=HMAC-SHA256-BASE64({secretKey}, {AuthPrefix} + "\n" + {Data})
    4、生成认证信息, 通过 Authorization header 传递        
     Authorization: {AuthPrefix}/{Signature}

     Example:
     1\应用 accessKey/secretKey 分别为 bTkALtTB9x6GAxmFi9wetAGH / PMROwlieALT36qfdGClVz2iH4Sv8xZxe
       POST 方式访问 http://api.ai.sogou.com/speech/asr 接口
       GET 参数为 type=gbk&idx=1&starttime=1491810516
       当前系统时间为 1491810516
     2\计算过程         
       {AuthPrefix}="sac-auth-v1/bTkALtTB9x6GAxmFi9wetAGH/1491810516/3600"
       {Data}="POST\napi.ai.sogou.com\n/speech/asr\nidx=1&starttime=1491810516&type=gbk"
       {Signature}=HMAC-SHA256-BASE64("PMROwlieALT36qfdGClVz2iH4Sv8xZxe", {AuthPrefix} + "\n" + {Data})="vuVEkzcnUeFv8FxeWS50c7S0HaYH1QKgtIV5xrxDY/s="
     3\最终生成的 header 为
       Authorization: sac-auth-v1/bTkALtTB9x6GAxmFi9wetAGH/1491810516/3600/vuVEkzcnUeFv8FxeWS50c7S0HaYH1QKgtIV5xrxDY/s=
    '''
    def get_auth_sign_str(self,url,method):
        res= parse.urlparse(url)
        host= res.netloc
        uri = res.path
        query= res.query
               
        
        #1生成前置字符串
        authprefix= 'sac-auth-v1/%s/%s/%s' %(self.__app_key,self.get_time_stamp(),3600)
        #2生成data
        query=dict( (k, v if len(v)>1 else v[0] )
                        for k, v in parse.parse_qs(res.query).items() )         
        sort_dict= sorted(query.items(), key=lambda item:item[0], reverse = False)
        sortquerystr= parse.urlencode(sort_dict)
        data= '%s\n%s\n%s\n%s' %(method,host,uri,sortquerystr)
        #3生成signstr
        signstr ='%s\n%s' %(authprefix,data)
        #调用hamc.sha256
        shastr =hmac.new(self.__app_secret.encode(), signstr.encode(), digestmod=hashlib.sha256).digest()
        #base64编码，还原成字符串
        signature = base64.b64encode(shastr).decode()
        
        #4组合成最终的授权码
        authstr= '%s/%s' %(authprefix,signature)
        return authstr

    '''
    $file = "OCR-test03.jpg";
    $url = "http://api.ai.sogou.com/pub/ocr";
    
    $hdr = array(
        "Content-Type: multipart/form-data",
        "Authorization: ".sign($ak, $sk, $url, "POST")
    ); // cURL headers for file uploading
    
    $postfields = array(
        "pic" => curl_file_create($file,'image/jpeg','a_b_c.jpg'),
    );
    
    $ch = curl_init();
    $options = array(
        CURLOPT_URL => $url,
        CURLOPT_HEADER => false,
        CURLOPT_POST => 1,
        CURLOPT_HTTPHEADER => $hdr,
        CURLOPT_POSTFIELDS => $postfields,
        CURLOPT_RETURNTRANSFER => true
    );
    '''
    def apiSougouOcr(self,apiname,picfilename):
        url = SougouAPI[apiname]['APIURL']
        name = SougouAPI[apiname]['APINAME']
        desc= SougouAPI[apiname]['APIDESC']
        
        authstr=self.get_auth_sign_str(url, method='POST')
        header={ "Authorization": authstr }
        
        picfile= {'pic':open(picfilename,'rb')}
        
        resp = requests.post(url,headers=header,files=picfile)           
        #print (resp.text)

