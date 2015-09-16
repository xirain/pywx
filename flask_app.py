# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import urllib2, json, urllib
import time

app = Flask(__name__)

@app.route('/weixin', methods=['GET'])
def weixin_verify():
    if request.method == 'GET':
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        token = 'testtest'
        tmplist = [token, timestamp, nonce]
        tmplist.sort()
        tmpstr = ''.join(tmplist)
        hashstr = hashlib.sha1(tmpstr).hexdigest()

        if hashstr == signature:
            return echostr #success
        return 'access verification fail' #fail

def getFanyi(word):
    word = urllib2.quote(word)
    # apiuri = 'http://fanyi.youdao.com/openapi.do?keyfrom=flaskr&key=1272049953&type=data&doctype=json&version=1.1&q={}'.format(word)
    handler=urllib2.HTTPHandler(debuglevel=1)
    opener = urllib2.build_opener(handler)
    urllib2.install_opener(opener)
    url = 'http://fanyi.youdao.com/openapi.do'
    values = {'keyfrom':'flaskr',
              'key':1272049953,
              'type':'data',
              'doctype':'json',
              'version':1.1,
              'q':word}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    try:
        resp = urllib2.urlopen(req)
        jsonData = json.loads(resp.read())

        # print json.dumps(jsonData,indent=2)
        errorCode = jsonData['errorCode']
        if 0 == errorCode:
            trans = u'\n{}的翻译：{}.\n 网络解释：{}\n'.format(jsonData['query'], ';'.join(jsonData['basic']['explains']), ';'.join(jsonData['web'][0]['value']))
        else:
            trans = u'翻译出错，错误码 {}'.format(errorCode)
    except Exception, e:
        trans = str(e)
    
    return trans


@app.route('/weixin', methods=['POST'])
def weixin_echo_you_said():
    str_xml = request.data
    xml = ET.fromstring(str_xml)
    content = xml.find("Content").text
    msg_type = xml.find("MsgType").text
    from_user = xml.find("FromUserName").text
    to_user = xml.find("ToUserName").text
    # msg_id = xml.find("MsgId").text

    if type(content).__name__ == "unicode":
            content = content.encode('UTF-8')
    content = getFanyi(content)
    response_data = """
<xml>
<ToUserName><![CDATA[{}]]></ToUserName>
<FromUserName><![CDATA[{}]]></FromUserName>
<CreateTime>{}</CreateTime>
<MsgType><![CDATA[{}]]></MsgType>
<Content><![CDATA[{}]]></Content>
<FuncFlag>0<FuncFlag>
</xml>
""".format(from_user,
    to_user,
    str(int(time.time())),
    msg_type,
    content)
    response = make_response(response_data)
    response.content_type = 'application/xml'
    return response

@app.route('/')
def hello_world():
    return 'Hello from Flask!'
