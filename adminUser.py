from datetime import datetime, timedelta
import datetime
import json
import requests
import pandas as pd
import calendar
import schedule
import time


class TelegramBot():
    def __init__(self):
        self._token = None 
        self._channel = None
        self._token = '5445102818:AAERt9dZd78Kyw5iWb66ZfIHU6T6DRyYTnk'
        self._group = '-600930539'

    def get_updates(self):
        url = f"https://api.telegram.org/bot{self._token}/getUpdates"
        data = {"allowed_updates": ["message", "edited_channel_post", "callback_query"]}
        #response = requests.get(url)

        response = requests.post(url, data=data)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def createChatInviteLink(self,chat_id):

        url = f"https://api.telegram.org/bot{self._token}/createChatInviteLink"

        horaActual = datetime.datetime.now()
        #pasado1Minute = horaActual + timedelta(minutes=1)

        date_example = str(horaActual.month) + '/' + str((horaActual.day)) + '/' + str(horaActual.year) + ', ' + str(horaActual.hour) + ':' + str(horaActual.minute + 1) + ':' + str(horaActual.second)
        print(date_example)
        date_format = datetime.datetime.strptime(date_example,
                                                "%m/%d/%Y, %H:%M:%S")
        unix_time = datetime.datetime.timestamp(date_format)

        print(unix_time)

        date_time = datetime.datetime.fromtimestamp(unix_time)
        
        # print unix time stamp
        print("Unix_Time =>",unix_time)
        
        # displaying date and time in a regular 
        # string format
        print("Date & Time =>" ,
        date_time.strftime('%Y-%m-%d %H:%M:%S'))

        data = {"chat_id": chat_id, "name": "RegisPrueba","expire_date": unix_time, "member_limit":1}


        response = requests.post(url, data=data)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        msg = f"Error code: {response.status_code}. Description: {response.text}"
        raise Exception(msg)

    def ChatMemberBanned(self,chat):

        url = f"https://api.telegram.org/bot{self._token}/ChatMemberBanned"

        data = {"user": chat_id, "until_date": "RegisPrueba","expire_date": unix_time, "member_limit":1}


        response = requests.post(url, data=data)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        msg = f"Error code: {response.status_code}. Description: {response.text}"
        raise Exception(msg)

if __name__ == '__main__':

    print("Generando Link")
    
    tb = TelegramBot()

    canal = "-1001390717517" 

    #print(tb.createChatInviteLink(canal))
    print(tb.get_updates())