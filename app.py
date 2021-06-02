#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np
import requests
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)
app = Flask(__name__)
lineaccesstoken = 'mjSxsXlCd85ns0d8mdIrZI3HJ55hGYV1MzWDqqiFM1txHUITTdaG12a5ws8/WhiGgthD7KfuLjgfgBM7UuxI8es7Pqwijx2gcaCedpp/EjVE0XLwOvGVDvL9JWrAfeP0MbEI0I6qg8OVIFlvhG9dXwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)
####################### new ########################
@app.route('/')
def index():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    copy = decoded
    i = 0
    while i < 5:
        no_event = len(copy['events'])
        for i in range(no_event):
            event = copy['events'][i]
            event_handle(event)
        i+=1
    return '',200

def cost():
    api_host = 'https://api.bitkub.com'
    response =  requests.get(api_host + '/api/market/ticker')
    result = response.json()
    lastest_cost = str(result['THB_DOGE']['last'])
    return lastest_cost
def event_handle(event):
    print(event)
    try:
        userId = event['source']['userId']
    except:
        print('error cannot get userId')
        return ''
    try:
        rtoken = event['replyToken']
    except:
        print('error cannot get rtoken')
        return ''
    try:
        msgId = event["message"]["id"]
        msgType = event["message"]["type"]
    except:
        print('error cannot get msgID, and msgType')
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
        return ''

    if msgType == "text":
        msg = str(event["message"]["text"])
        if msg == "ราคา doge":
            final_result = cost()
            replyObj = TextSendMessage(text=final_result)
            line_bot_api.reply_message(rtoken, replyObj)
            

        else:
            replyObj = TextSendMessage(text=msg)
            line_bot_api.reply_message(rtoken, replyObj)
    else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj)
    return ''
if __name__ == '__main__':
    app.run(debug=True)