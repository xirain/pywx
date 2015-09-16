# -*- coding: utf-8 -*-
# A very simple Flask Hello World app for you to get started with...
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask, request, make_response
import hashlib
# import lxml
import time
# import os
# import urllib2,json
# from lxml import etree
import xml.etree.ElementTree as ET

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
    # elif request.method == 'POST':
    #     # xml_recv = ET.fromstring(request.data)
    #     # ToUserName = xml_recv.find("ToUserName").text
    #     # FromUserName = xml_recv.find("FromUserName").text
    #     # Content = xml_recv.find("Content").text
    #     #
    #     # reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    #     # response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content ) )
    #     # response.content_type = 'application/xml'
    #     # return response
    #     str_xml = request.data
    #     xml = ET.fromstring(str_xml)
    #     content = xml.find("Content").text
    #     # msg_type = xml.find("MsgType").text
    #     from_user = xml.find("FromUserName").text
    #     to_user = xml.find("ToUserName").text
    #     # # msg_id = xml.find("MsgId").text

    #     response_data = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    #     response = make_response(response_data  % (from_user, to_user, str(int(time.time())), u'我现在还在开发中，还没有什么功能，您刚才说的是： '+(content)))
    #     response.content_type = 'application/xml'
    #     return response

@app.route('/weixin', methods=['POST'])
def weixin_echo_you_said():
    str_xml = request.data
    xml = ET.fromstring(str_xml)
    content = xml.find("Content").text
    msg_type = xml.find("MsgType").text
    from_user = xml.find("FromUserName").text
    to_user = xml.find("ToUserName").text
    # msg_id = xml.find("MsgId").text

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
    u"我现在还在开发中，还没有什么功能，您刚才说的是：" + content)
    response = make_response(response_data)
    response.content_type = 'application/xml'
    return response

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

