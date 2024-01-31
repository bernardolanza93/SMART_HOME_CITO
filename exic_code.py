import Adafruit_DHT
import RPi.GPIO as GPIO
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, KeyboardButton
from telepot.loop import MessageLoop
from gpiozero import CPUTemperature
import time
from time import sleep
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import socket
import psutil
from simple_scaraper_portfolio import *

import multiprocessing
import os
import cv2
import logging

import reciver

import csv
import pandas as pd


string_from_tcp_ID = "null"
path_here = os.getcwd()
path = path_here + "/data/"
bernardo_chat_id = "283149655"


def aggiungi_utente_autorizzato(chat_id, nome):
    if os.path.exists("utenti_autorizzati.json"):
        with open("utenti_autorizzati.json", "r") as file:
            utenti_autorizzati = json.load(file)
        utenti_autorizzati[chat_id] = nome
        with open("utenti_autorizzati.json", "w") as file:
            json.dump(utenti_autorizzati, file)
        print(f"Utente aggiunto: {nome} (ID Chat: {chat_id})")
    else:
        print("Il file utenti_autorizzati.json non esiste. Creare il file prima di aggiungere nuovi utenti.")

def controllo_autorizzazione_utente(chat_id):
    with open("utenti_autorizzati.json", "r") as file:
        utenti_autorizzati = json.load(file)
        if chat_id in utenti_autorizzati:
            return 1, utenti_autorizzati[chat_id]
        else:
            return 0, None

# Our "on message" eventù

def crea_file_utenti_autorizzati():
    if not os.path.exists("utenti_autorizzati.json"):
        utenti_autorizzati = {
            "283149655": "bernardo",
            "505937736": "alessandro"
        }
        with open("utenti_autorizzati.json", "w") as file:
            json.dump(utenti_autorizzati, file)
        print("File utenti_autorizzati.json creato.")



def check_folder(relative_path):
    """
    check_folder : check  the existence and if not, create the path for the results folder

    :param relative_path:path to be checked


    :return nothing:
    """

    workingDir = os.getcwd()
    path = workingDir + relative_path

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)

        print("The new directory is created!", path)
    else:
        print('directory ok:', path)






def make_graph():

    headers = ['data','temp','hum']
    df = pd.read_csv('temp_dataRPCITO.csv',names=headers)
    print (df)

    df['data'] = df['data'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
    x = df['data']
    y = df['temp']
    z = df['hum']


    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('time',rotation=45)
    ax1.set_ylabel('Temp', color=color)
    ax1.plot(x, y, color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)
    ax1.tick_params(axis='x', labelrotation=45)
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('hum', color=color)  # we already handled the x-label with ax1
    ax2.plot(x,z, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    # otherwise the right y-label is slightly clipped
    
    plt.savefig('plot_data_citofono.png')
    plt.close("all")
    #The simplest way is to start the ntetwork loop on a separate thread using the client.loop_start() function, then use the normal client.publish method


def write_data_csv():
    
    while True:
        # Get the current time
        current_time = datetime.now().time()

        # Check if it's after 8 AM
        if current_time.hour >= 8:
            controlla_file()
        time.sleep(10)
        

#plt.show()



# when connecting to mqtt do this;
# receive messages on this topic

    
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    autorizzazione, nome = controllo_autorizzazione_utente(chat_id)

    who = msg['from']['first_name']
    bot.sendMessage(chat_id, "Hi" + str(who))
    bot.sendMessage(chat_id, "you say:")
    bot.sendMessage(chat_id, msg['data'])
    if not autorizzazione:

        if msg['data']  == 'Juve':
            bot.sendMessage(chat_id, "you said well" + str(who) + " .FORZA JUVE SEMPRE // AUTHORIZED")
        else:
            bot.sendMessage(chat_id, "NOT AUTHORIZED ILLEGAL USE OF THE BOT")
            bot.sendMessage(chat_id, "CALLING CARABINIERI  113....")
    else:

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                        [InlineKeyboardButton(text="INFO",callback_data='info'),
                                         InlineKeyboardButton(text="CANCELLO",callback_data='open1'),
                                         InlineKeyboardButton(text="CRYPTO", callback_data='status'),
                                         InlineKeyboardButton(text="REBOOT", callback_data='open2')
                                         ]

                                    ]
                                )

        bot.sendMessage(chat_id, "OPZIONI CASA SMART:", reply_markup=keyboard)


        print("||_||_ CHECK BOT MENU")

def on_callback_query(msg):

    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    file_path = '/home/pi/plot_data_citofono.png'
    file_path1 = '/home/pi/plot_rec.png'
    info = bot.getChat(chat_id)


    respond = 0

    autorizzazione, nome = controllo_autorizzazione_utente(chat_id)


    if not autorizzazione:
        #manda a me
        bot.sendMessage(bernardo_chat_id, " the user "+ str(chat_id) + " says :" + str(msg))

        #risponde a lui
        if str(msg) == "Juve":
            bot.sendMessage(chat_id, "you said well" + str(chat_id) + " .FORZA JUVE SEMPRE")
            bot.sendMessage(chat_id, "WELCOME STRANGER!" )
            respond = 1
        else:
            bot.sendMessage(chat_id, "You said:")
            bot.sendMessage(chat_id, msg)
            bot.sendMessage(chat_id, "NOT AUTHORIZED ILLEGAL USE OF THE BOT")
            bot.sendMessage(chat_id, "CALLING CARABINIERI  113....")
            respond = 0


    else:

        bot.sendMessage(chat_id, "Hi Bernardo SUPERUSER! My Master :)")
        respond = 1







    if autorizzazione == 1:

        if query_data=='info':
            print("||_||_ CHECK INFO LOG")
            bot.sendMessage(chat_id, "CHAT:")
            bot.sendMessage(chat_id, str(chat_id))

            now = datetime.now()
            hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
            cpu = CPUTemperature()
            bot.sendMessage(chat_id, 'CPU_temp citofono: %s'%str(cpu.temperature))
            bot.sendMessage(chat_id, str(hourstr))
            bot.sendDocument(chat_id, open(path + "RPI_SH.log", 'rb'))
            loggingR.error("(info)______________________EVENT____________________")

            loggingR.error("INFO RICHIESTE____time: %s", str(hourstr))

            loggingR.error("UTENTE: %s", str(info))

            print("||_||_ CHECK STATUS")
            bot.sendMessage(chat_id, "data from the raspi...")
            username = os.getlogin()
            bot.sendMessage(chat_id, "username")
            bot.sendMessage(chat_id, username)

            # Get the hostname
            hostname = socket.gethostname()
            # Get the IP address
            ip_address = socket.gethostbyname(hostname)
            bot.sendMessage(chat_id, "hostname")
            bot.sendMessage(chat_id, hostname)
            bot.sendMessage(chat_id, "ip_address")
            bot.sendMessage(chat_id, ip_address)

            # Current process ID
            current_pid = os.getpid()
            bot.sendMessage(chat_id,"Current Process ID: ")
            bot.sendMessage(chat_id,current_pid)
            # Parent process ID
            parent_pid = os.getppid()
            bot.sendMessage(chat_id,"Parent Process ID: ")
            bot.sendMessage(chat_id,parent_pid)



        elif query_data=='open1':
            print("||_||_ CHECK CANCELLO")

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(3, GPIO.OUT)
            GPIO.output(3, GPIO.HIGH)
            GPIO.output(3, GPIO.LOW)
            sleep(1)
            GPIO.output(3, GPIO.HIGH)
            bot.sendMessage(chat_id, "apertura cancello...")
            now = datetime.now()
            hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
            loggingR.error("(open1)______________________EVENT____________________")

            loggingR.error("APERTURA CANCELLO____time: %s", str(hourstr))
            loggingR.error("UTENTE: %s", str(info))
            bot.sendMessage(chat_id, "ID CHAT:")
            bot.sendMessage(chat_id, str(chat_id))


        elif query_data=='open2':

            print("||_||_ CHECK REBOOT")
            bot.sendMessage(chat_id, "reboot in corso...")
            os.system('sudo reboot')
            now = datetime.now()
            hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
            loggingR.error("(open2)______________________EVENT____________________")
            loggingR.error("APERTURA CANCELLO____time: %s", str(hourstr))
            loggingR.error("UTENTE: %s", str(info))


        elif query_data=='status':


            crypto_string = leggi_stringa_oggi()
            # plot_andamento_cripto(nome_crypto, crypto_portfolio)
            for info in crypto_string:
                bot.sendMessage(chat_id,info)





def bot_ini(bot):

    MessageLoop(bot, {'chat': on_chat_message,
      'callback_query': on_callback_query}).run_as_thread()
    print("||_||_ CHECK BOT ONLINE")
    while True:
        sleep(2)

        print(".",end='')
    


now = datetime.now()
hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
print("||_||_ CHECK FOLDER")
check_folder("/data/")
print("||_||_ CHECK LOGGER")
try:
    loggingR = logging.getLogger('RPI')
    loggingR.setLevel(logging.INFO)
    fh = logging.FileHandler('./data/RPI_SH.log')
    fh.setLevel(logging.DEBUG)
    loggingR.addHandler(fh)

    loggingR.error("STARDED LOGGING FILE____time: %s", str(hourstr))
except Exception as e:
    print("ERROR LOGGING: ", e)


sensor = Adafruit_DHT.DHT11
pin = 4



print("||_||_ CHECK BOT")
humidity = 0.0
temperature = 0.0
bot = telepot.Bot('2070265556:AAHtStxZRT_J9hxvBtC7EKdnfM6sXVOgJ4U')

loggingR.error("INI____ALL(4 yeah) PROCs: %s", str(hourstr))
print("||_||_ CHECK PROCESSES")
p1 = multiprocessing.Process(target=reciver.listen_for_TCP_string, args=(string_from_tcp_ID,))
p2 = multiprocessing.Process(target=bot_ini,args = (bot,))
p3_ri = multiprocessing.Process(target=reciver.main)
p_sensor = multiprocessing.Process(target=write_data_csv)


try:
    p1.start()
except Exception as e:
    loggingR.error("PROCESS error 1:  %s ", e)
try:
    p2.start()
except Exception as e:
    loggingR.error("PROCESS error 2:  %s ", e)
try:

    p3_ri.start()
except Exception as e:
    loggingR.error("PROCESS error 3:  %s ", e)

try:

    p_sensor.start()
except Exception as e:
    loggingR.error("PROCESS error 4:  %s ", e)
print("||_||_ CHECK START PROCESS")

print("ID of process p1: {}".format(p1.pid))
print("ID of process p1: {}".format(p2.pid))
print("ID of process p1: {}".format(p3_ri.pid))
print("ID of process p1: {}".format(p_sensor.pid))

p1.join()
p2.join()
p3_ri.join()
p_sensor.join()
