#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import time
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
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        use_infor = event_handle(event)
        process(use_infor)
        
    return '',200

def cost():
    api_host = 'https://api.bitkub.com'
    response =  requests.get(api_host + '/api/market/ticker')
    result = response.json()
    lastest_cost = result['THB_DOGE']['last']
    buy_cost = 12.72
    buy_money = 42332.87
    want_sell = (lastest_cost / buy_cost) * buy_money
    status = ""
    if want_sell > buy_money:
        status = 'กำไร'
    elif want_sell == buy_money:
        status = 'เสมอทุน'
    else:
        status = 'ขาดทุน'
    sell_profit = want_sell - buy_money
    percent = (sell_profit / buy_money) * 100

    result = f'ตอนนี้ราคา DOGE: {lastest_cost} บาท\n\nซื้อมาที่ {buy_money:,} บาท\n\nถ้าขายจะได้ {sell_profit:,.2f} บาท คิดเป็น{status}\n{percent:.2f}%' 

    return result

def event_handle(event):
    print(event)
    infor_list = []
    try:
        userId = event['source']['userId']
        infor_list.append(userId)
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
    infor_list.append(event["message"]["text"])

    return infor_list
    
def process(use_infor):

    if use_infor[1] == "ราคา":
        i = 0
        while i < 7:
            line_bot_api.push_message(use_infor[0], TextSendMessage(text=cost()))
            time.sleep(1)
            i += 1
        
    """ else:
        sk_id = np.random.randint(1,17)
        replyObj = StickerSendMessage(package_id=str(1),sticker_id=str(sk_id))
        line_bot_api.reply_message(rtoken, replyObj) """
    
    #return ''
if __name__ == '__main__':
    app.run(debug=True)