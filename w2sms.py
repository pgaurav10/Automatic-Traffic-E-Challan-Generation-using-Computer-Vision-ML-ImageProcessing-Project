# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:38:49 2019

@author: Prathamesh
"""

import requests


def send(ph, message):
    URL = 'https://www.way2sms.com/api/v1/sendCampaign'
    
    # get request
    def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
      req_params = {
      'apikey':apiKey,
      'secret':secretKey,
      'usetype':useType,
      'phone': phoneNo,
      'message':textMessage,
      'senderid':senderId
      }
      return requests.post(reqUrl, req_params)
    # get response
    response = sendPostRequest(URL, '4TMBM9PMBZ5ZQKNK8S7P8YBJ0HUR0BO4', '4H62G6QKQSHOM037', 'stage', ph, '8605511687', message)
    """
      Note:-
    you must provide apikey, secretkey, usetype, mobile, senderid and message values
    and then requst to api
    """
    # print response if you want