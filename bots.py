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
        self._group = None
        self._channel = None
        self._channel2 = None

        # Todos estos ID se sacan  mediante https://api.telegram.org/bot{self._token}/getUpdates
        # Example en este caso: https://api.telegram.org/bot5445102818:AAERt9dZd78Kyw5iWb66ZfIHU6T6DRyYTnk/getUpdates


        self._token = '5445102818:AAERt9dZd78Kyw5iWb66ZfIHU6T6DRyYTnk'
        # Para sacar este primero anadimos el bots a un grupo para que podamos copiar el ID de; chat_id del grupo
        self._group = '-600930539'
        # Para sacar este primero anadimos el bots a un canal para que podamos copiar el ID del chat_id del canal

        #self._channel = '-1001390717517' # TELEGRAM PRUEBAS 

        #self._channel = '-1001658019906' #TELEGRAM PRODUCCION

        

        #1001713120047

    def get_me(self):
        url = f"https://api.telegram.org/bot{self._token}/getMe"
        response = requests.get(url)
        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def get_updates(self):
        url = f"https://api.telegram.org/bot{self._token}/getUpdates"
        response = requests.get(url)
        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        return None

    def send_message_to_group(self, message, parse_mode='HTML'):
        try:
            return self.send_message(self._group, message, parse_mode)
        except Exception as exception:
            print(exception)
        return None

    def send_message_to_channel(self, message, parse_mode='HTML'):
        try:
            return self.send_message(self._channel, message, parse_mode)
        except Exception as exception:
            print(exception)
        return None

    def send_message(self, chat_id, message, parse_mode='HTML'):
        url = f"https://api.telegram.org/bot{self._token}/sendMessage"
        data = {"chat_id": chat_id, "text": message, "parse_mode": parse_mode}
        response = requests.post(url, data=data)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        msg = f"Error code: {response.status_code}. Description: {response.text}"
        raise Exception(msg)

    def send_photo(self, chat_id, filename, caption, parse_mode='HTML'):

        url = f"https://api.telegram.org/bot{self._token}/sendPhoto"

        data = {"chat_id": chat_id, "caption": caption,"parse_mode": parse_mode}

        files = {"photo": (filename, open(filename, 'rb'))}

        response = requests.post(url, data=data, files=files)

        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        msg = f"Error code: {response.status_code}. Description: {response.text}"
        raise Exception(msg)

    def send_photo_to_channel(self, filename, caption, canal):
        try:

            return self.send_photo(canal, filename, caption)

            #return self.send_photo(self._channel, filename, caption)
        except Exception as exception:
            print(exception)
        return None

    def send_photo_to_group(self, filename, caption):
        try:
            return self.send_photo(self._group, filename, caption)
        except Exception as exception:
            print(exception)
        return None

    def __post(self, url, data, files=None):
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            salida = json.loads(response.text)
            return salida
        error = json.loads(response.text)
        error_code = error['error_code']
        description = error['description']
        msg = f"Error: {error_code}. Description: {description}"
        raise Exception(msg)
        
    def send_document(self, filename, caption, chat_id=None):
        chat_id = chat_id if chat_id else self._channel
        url = f"https://api.telegram.org/bot{self._token}/sendDocument"
        data = {"chat_id": chat_id, "caption": caption}
        files = {"document": (filename, open(filename, 'rb'))}
        return self.__post(url, data, files)

    def send_dice(self, emoji=None, chat_id=None):
        chat_id = chat_id if chat_id else self._channel
        url = f"https://api.telegram.org/bot{self._token}/sendDice"
        data = {"chat_id": chat_id, "emoji": emoji} 
        return self.__post(url, data)


if __name__ == '__main__':

    print("Corriendo robot de Telegram - BetSolver VERSION 1.1.2 ......................................................................................")
    
    tb = TelegramBot()

    def envioGeneral(url,nombreEstrategia,Tipofiltro,minutosEnv,canalID = 1):
        try:

            filtro = ""
            canal = canalID

            if(Tipofiltro == 1):
                filtro = "Filtro 1"
            elif(Tipofiltro == 2):
                filtro = "Filtro 2"
            elif(Tipofiltro == 3):
                filtro = "Filtro 3"
            elif(Tipofiltro == 4):
                filtro = "Filtro 4"
            elif(Tipofiltro == 5):
                filtro = "Filtro 5"
            elif(Tipofiltro == 6):
                filtro = "Filtro 6"


                
            df = pd.read_excel(url, sheet_name=nombreEstrategia)

            if(df.empty):

                return None

            else:
            
                hora_Actual = datetime.datetime.now()
                horaActual = hora_Actual + datetime.timedelta(minutes=minutosEnv)
                horaActual =  horaActual.strftime('%H:%M:00')
                fechaActual = datetime.datetime.now().strftime('%d.%m.%Y')
                fechaCompleta = fechaActual + ' ' + horaActual;


                #Hago esto porque aveces el formato de la fecha viene en string o en datetime, cuando viene en datatime pasa bien pero cuando 
                #viene como string se deben agregar :00 al final
                for i in df.index:     
                    lenHora = (len(str(df["Hora"][i])))
                    if(lenHora == 5):
                        df.at[i,'Hora'] =  df['Hora'][i] + ':00'
          

                df['Hora'] = pd.to_datetime(df.Hora, format="%H:%M:%S")
                df['Fecha'] = pd.to_datetime(df.Fecha, format='%Y%m%d', errors='ignore')
                df["DateStr"] = df['Fecha'] + ' ' + df['Hora'].dt.strftime("%H:%M:%S")

                partidosFiltroFecha = df['DateStr'] == fechaCompleta

                partidosYa = df[partidosFiltroFecha]

                if partidosYa.empty:
                    return None
                else:

                    lista = partidosYa.to_numpy().tolist();

                    for x in lista:

                        if(nombreEstrategia == "Local Estrategia 5.5"): #GANA EMPATE LOCAL
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia15FullTimeMarkBroken.jpg", cadena, canal)


                        if(nombreEstrategia == "Visitante  Estrategia 5.5"): #GANA EMPATE VISITANTE
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/ImageEstrategiaOver1_5VisitanteFavorito.jpeg", cadena, canal)

                        if(nombreEstrategia == "Local Estrategia 3.5"): #DOS GOLES PRIMER TIEMPO HT 
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/UnGolOMasPrimerTiempo0_5HT_MatBroker.jpg", cadena, canal)

                            
                        if(nombreEstrategia == "Visitante  Estrategia 3.5"): #DOS GOLES PRIMER TIEMPO HT 
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/UnGolOMasPrimerTiempo0_5HT_MatBroker.jpg", cadena, canal)

           
                        if(nombreEstrategia == "Local Estrategia 3"): #DOS GOLES PRIMER TIEMPO HT LOCAL 
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/UnGolOMasPrimerTiempo0_5HT_MatBroker.jpg", cadena, canal)

                        if(nombreEstrategia == "Visitante  Estrategia 3"): #DOS GOLES PRIMER TIEMPO HT VISITANTE
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[9] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[9] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/UnGolOMasPrimerTiempo0_5HT_MatBroker.jpg", cadena, canal)
               
                        if(nombreEstrategia == "Local Estrategia 5"):     
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia15FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Visitante  Estrategia 5"):     
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia15FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Local Estrategia 4"):     
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/TresMasGoles.jpeg", cadena, canal)
                        
                        if(nombreEstrategia == "Visitante  Estrategia 4"):     
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/TresMasGoles.jpeg", cadena, canal)   


                        if(nombreEstrategia == "Local Estrategia 2"):       
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpeg", cadena, canal) 

                        if(nombreEstrategia == "Visitante  Estrategia 2"): 
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)  
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpeg", cadena, canal)  

                        if(nombreEstrategia == "Local Estrategia 8"):       
                            print("Se envio " + "Liga: " + str(x[3]) + " Local: " + x[4] + " Visitante: " +  x[5] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[2].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[3]) + "\n" + "<b>🤑Local: </b>" + x[4] + "\n" + "<b>🤑Visitante: </b>" +  x[5] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)                           
                        
                        if(nombreEstrategia == "Visitante  Estrategia 8"):       
                            print("Se envio " + "Liga: " + str(x[3]) + " Local: " + x[4] + " Visitante: " +  x[5] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[2].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[3]) + "\n" + "<b>🤑Local: </b>" + x[4] + "\n" + "<b>🤑Visitante: </b>" +  x[5] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Visitante  Estrategia 0"):       
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)   
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Local Estrategia 0"):      
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)    
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)
                        
                        if(nombreEstrategia == "Visitante  Estrategia 6"):       
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)   
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Local Estrategia 6"):      
                            print("Se envio " + "Liga: " + str(x[2]) + " Local: " + x[3] + " Visitante: " +  x[4] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)    
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[1].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[2]) + "\n" + "<b>🤑Local: </b>" + x[3] + "\n" + "<b>🤑Visitante: </b>" +  x[4] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia05FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Partidos Local Patrones"):      
                            print("Se envio " + "Liga: " + str(x[3]) + " Local: " + x[4] + " Visitante: " +  x[5] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)    
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[2].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[3]) + "\n" + "<b>🤑Local: </b>" + x[4] + "\n" + "<b>🤑Visitante: </b>" +  x[5] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/estrategia15FullTimeMarkBroken.jpg", cadena, canal)

                        if(nombreEstrategia == "Partidos Visitante Patrones"):      
                            print("Se envio " + "Liga: " + str(x[3]) + " Local: " + x[4] + " Visitante: " +  x[5] + " " + nombreEstrategia + " con " + filtro + ". Hora del partido: " + horaActual)    
                            cadena = "Apuesta en vivo 🔥" +  "\n" + "<b>🔊Fecha: </b>" + str(x[0]) + "\n" + "<b>🚨Hora: </b>" + str(x[2].strftime("%H:%M:%S")) + "\n" + "<b>⚽️Liga: </b>" + str(x[3]) + "\n" + "<b>🤑Local: </b>" + x[4] + "\n" + "<b>🤑Visitante: </b>" +  x[5] + "\n"
                            cadena += "<a  target='_blank' href='https://app.afiliago.com/paygo/markbroker'>ENTRA AQUÍ YA..!! GRUPO VIP</a>"
                            tb.send_photo_to_channel("../Futbol/Imagenes/ImageEstrategiaOver1_5VisitanteFavorito.jpeg", cadena, canal)
                        
        

        except Exception as exception:
            print('Error: ' + nombreEstrategia)
            print(exception)

    
    filtro1 = R'../Futbol/Partidos_estrategias filtro 1.xlsx'
    filtro2 = R'../Futbol/Partidos_estrategias filtro 2.xlsx'
    filtro3 = R'../Futbol/Partidos_estrategias Filtro 3.xlsx'
    filtro4 = R'../Futbol/Partidos_estrategias Filtro 4.xlsx'
    filtro5 = R'../Futbol/Partidos_estrategias Filtro 5.xlsx'
    filtro6 = R'../Futbol/Partidos_estrategias Filtro 6.xlsx'

    filtroPatrones = R'../Futbol/Listado_partidosPatrones.xlsx'

            
    BetSolver_05_HT_un_gol_o_mas_1_tiempo = "-1001731867847"

    BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO = "-1001648801892"

    Betsolver_FullTime_25_TresOMasGolesPartido = "-1001697918027" 

    BetSolver_Over_05_UnGolOmasPartido = "-1001713120047" 

    BetSolver_EquiposFavOver1_5 ="-1001390717517"

    #Estan van por el telegram real
    #Funciom, excel, Nombre estrategia, tipo filtro, minutos antes o  despues, canal.

    schedule.every(1).minute.do(envioGeneral,filtro1,"Local Estrategia 5.5",1,-80,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)
    schedule.every(1).minute.do(envioGeneral,filtro1,"Visitante  Estrategia 5.5",1,-80,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)

    schedule.every(1).minute.do(envioGeneral,filtro2,"Local Estrategia 3",2,-17,BetSolver_05_HT_un_gol_o_mas_1_tiempo)
    schedule.every(1).minute.do(envioGeneral,filtro2,"Visitante  Estrategia 3",2,-17,BetSolver_05_HT_un_gol_o_mas_1_tiempo)

    schedule.every(1).minute.do(envioGeneral,filtro2,"Local Estrategia 3.5",2,-17,BetSolver_05_HT_un_gol_o_mas_1_tiempo) 
    schedule.every(1).minute.do(envioGeneral,filtro2,"Visitante  Estrategia 3.5",2,-17,BetSolver_05_HT_un_gol_o_mas_1_tiempo)

    schedule.every(1).minute.do(envioGeneral,filtro3,"Local Estrategia 5",3,-38,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)
    schedule.every(1).minute.do(envioGeneral,filtro3,"Visitante  Estrategia 5",3,-38,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)

    schedule.every(1).minute.do(envioGeneral,filtro3,"Local Estrategia 5",3,-80,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)
    schedule.every(1).minute.do(envioGeneral,filtro3,"Visitante  Estrategia 5",3,-80,BetSolver_15_FT_FULLTIME_DOSOMASGOLESENELPARTIDO)

    schedule.every(1).minute.do(envioGeneral,filtro3,"Local Estrategia 4",3,-17,Betsolver_FullTime_25_TresOMasGolesPartido)
    schedule.every(1).minute.do(envioGeneral,filtro3,"Visitante  Estrategia 4",3,-17,Betsolver_FullTime_25_TresOMasGolesPartido)

    schedule.every(1).minute.do(envioGeneral,filtro4,"Local Estrategia 0",4,-80,BetSolver_Over_05_UnGolOmasPartido)
    schedule.every(1).minute.do(envioGeneral,filtro4,"Visitante  Estrategia 0",4,-80,BetSolver_Over_05_UnGolOmasPartido)

    # schedule.every(1).minute.do(envioGeneral,filtro4,"Local Estrategia 2",4,-80,BetSolver_Over_05_UnGolOmasPartido)
    # schedule.every(1).minute.do(envioGeneral,filtro4,"Visitante  Estrategia 2",4,-80,BetSolver_Over_05_UnGolOmasPartido)

    schedule.every(1).minute.do(envioGeneral,filtro5,"Local Estrategia 8",5,-80,BetSolver_Over_05_UnGolOmasPartido)
    schedule.every(1).minute.do(envioGeneral,filtro5,"Visitante  Estrategia 8",5,-80,BetSolver_Over_05_UnGolOmasPartido)

    schedule.every(1).minute.do(envioGeneral,filtro6,"Local Estrategia 6",6,-80,BetSolver_Over_05_UnGolOmasPartido)
    schedule.every(1).minute.do(envioGeneral,filtro6,"Visitante  Estrategia 6",6,-80,BetSolver_Over_05_UnGolOmasPartido)


    schedule.every(1).minute.do(envioGeneral,filtroPatrones,"Partidos Local Patrones",3,-70,BetSolver_EquiposFavOver1_5)
    schedule.every(1).minute.do(envioGeneral,filtroPatrones,"Partidos Visitante Patrones",3,-70,BetSolver_EquiposFavOver1_5)




    while True:
        schedule.run_pending()
        time.sleep(1)


