#coding:utf-8
import re
import requests
import urllib

global s
s=requests.Session()

header={ "Accept":"text/plain, */*; q=0.01",
         "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0",
         "Host":"passport.jd.com",
         "Proxy-Connection":"keep-alive",
         "Accept-Language":"zh-cn",
         'Connection': 'keep-alive',
         'Referer': 'http://passport.jd.com/uc/login?ltype=logout',
         "Length":0
         }
def getHtml(url):
    global s
    headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'}
    req=s.get(url,headers=headers)
    req.encoding='gbk'
    return req.text

def getCodeUrl(html):
    res=re.findall(r'src2="(.*?)"',html)
    codeUrl=res[0]
    codeUrl=codeUrl.replace("amp;","")
    return codeUrl

def getCheckCode(url):
    response=requests.get(url)
    status=response.status_code
    picData=response.content
    path='D:/code.jpg'

    if status==200:
        localpic=open(path,'wb')
        localpic.write(picData)
        localpic.close()
        print "please go to the %s to open the image" %path
    else:
        print "failed to get the Check Code,status",status

def getUuidAndCode(html):
    reguuid=r'id="uuid" name="uuid" value="(\S+)"'
    patternuuid=re.compile(reguuid)
    res=patternuuid.findall(html)
    if res is not None:
        uuid=res[0]
    regCode=r'input type="hidden" name="(\S+)" value="(\S+)"'
    patternCode=re.compile(regCode)
    resCode=patternCode.findall(html)
    if resCode is not None:
        l0=resCode[0][0]
        l1=resCode[0][1]
    return (uuid,l0,l1)

def getPostData(uuid,l0,l1):
    data={
    "uuid":uuid,
    "machineNet":"",
    "machineCpu":"",
    "machineDisk":"",
    "loginname":username,
    "nloginpwd":password,
    "loginpwd":password,
    "chkRememberMe":"off",
    "authcode":"",
    l0:l1
    }
    return data

url='http://passport.jd.com/uc/login'
postUrl="http://passport.jd.com/uc/loginService"

html = getHtml(url)
urlcode=getCodeUrl(html)
uuid,l0,l1=getUuidAndCode(html)
data=getPostData(uuid,l0,l1)
print urlcode
getCheckCode(urlcode)
codeChar=raw_input("please input the code:")
data["authcode"]=codeChar
print data
datalen=len(urllib.urlencode(data))
header['Length']=datalen
ret=s.post(postUrl,data,headers=header)
print ret.text.decode("unicode_escape")

