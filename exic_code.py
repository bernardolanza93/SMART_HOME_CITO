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
from CONSTANT import *

import multiprocessing
import os
import cv2
import logging
import csv
import pandas as pd


keyboard_1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="INFO", callback_data='info'),
     InlineKeyboardButton(text="CANCELLO", callback_data='open1'),
     InlineKeyboardButton(text="CRYPTO", callback_data='crypto'),
     InlineKeyboardButton(text="REBOOT", callback_data='open2')
     ]

]
)


# Funzione per inviare un'immagine tramite Telepot
def invia_immagine(chat_id, image_path, bot):
    with open(image_path, 'rb') as image_file:
        bot.sendPhoto(chat_id, image_file)

# Funzione per inviare tutte le immagini presenti in una cartella
def invia_immagini_in_cartella(cartella, chat_id, bot):
    # Verifica se la cartella esiste
    if not os.path.exists(cartella):
        print(f"La cartella '{cartella}' non esiste.")
        return

    # Cicla su tutti i file nella cartella
    for filename in os.listdir(cartella):
        # Verifica se il file è un'immagine
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(cartella, filename)
            # Invia l'immagine
            invia_immagine(chat_id, image_path, bot)


def create_inline_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='PORTFOLIO', callback_data='data'),
        InlineKeyboardButton(text='UPDATE', callback_data='update'),
        InlineKeyboardButton(text='MOVES', callback_data='movers'),
        InlineKeyboardButton(text='<-', callback_data='back_to_main_menu')]
    ])
    return keyboard



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
        if str(chat_id) in utenti_autorizzati:
            print("AUTOR:", utenti_autorizzati, str(chat_id))
            return 1, utenti_autorizzati[str(chat_id)]

        else:
            print("NOT:", utenti_autorizzati, str(chat_id))
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





def write_data_csv(bot):



    bot.sendMessage(bernardo_chat_id, "TRADER BOT READY - BOOT FREE LOOP")
    try:
        initial_symbols = get_binance_symbols()
    except Exception as e:
        bot.sendMessage(bernardo_chat_id, "ERROR BINANCE SYMBOL:" + str(e))




    while True:
        try:

            current_symbols = get_binance_symbols()

            # Trova le nuove criptovalute aggiunte rispetto all'elenco iniziale
            new_symbols = set(current_symbols) - set(initial_symbols)

            if new_symbols:
                bot.sendMessage(bernardo_chat_id, "NEW CRYPTO:")

                for symbol in new_symbols:
                    bot.sendMessage(bernardo_chat_id, symbol)

                initial_symbols = current_symbols

                    # Aumenta il contatore ad ogni iterazione del ciclo
        except Exception as e:
            bot.sendMessage(bernardo_chat_id, "ERROR NEW SYMBOL :" + str(e))

        try:

            # Get the current time
            current_time = datetime.now().time()


            # Check if it's after 8 AM
            if current_time.hour >= 8:
                controlla_file()
        except Exception as e:
            bot.sendMessage(bernardo_chat_id, "ERROR MORNING ROUTINE SCRAPING :" + str(e))




        time.sleep(20)
        

#plt.show()



# when connecting to mqtt do this;
# receive messages on this topic

    
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    rispondi = 0
    autorizzazione, nome = controllo_autorizzazione_utente(chat_id)
    print(msg)
    print(type(msg))
    print(msg['from'])
    who = msg['from']['first_name']
    what = msg['text']

    bot.sendMessage(chat_id, "Hi " + str(who) + " you say:" +str(what))

    if not autorizzazione:
        bot.sendMessage(bernardo_chat_id,   str(who) + " says: " + str(what) + "[SU-COM]")

        if str(what)  == 'Juve':
            bot.sendMessage(chat_id, "you said well" + str(who) + " .FORZA JUVE SEMPRE // AUTHORIZED")
            rispondi = 1
        else:
            bot.sendMessage(chat_id, "NOT AUTHORIZED ILLEGAL USE OF THE BOT")
            bot.sendMessage(chat_id, "CALLING CARABINIERI  113....")
            rispondi = 0
    else:
        bot.sendMessage(chat_id, "BENTORNATO "+ str(who))
        rispondi = 1


    if rispondi:
        if str(what.split("_")[0]) == 'plot':
            crypto_plot = what.split("_")[1]
            invia_immagine(chat_id, FOLDER_GRAPH + "/" + crypto_plot + PLOT_STRING_TITLE,bot)


        bot.sendMessage(chat_id, "OPZIONI CASA SMART:", reply_markup=keyboard_1)


        print("||_||_ CHECK BOT MENU")

def on_callback_query(msg):

    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    file_path = '/home/pi/plot_data_citofono.png'
    file_path1 = '/home/pi/plot_rec.png'
    info = bot.getChat(chat_id)












    if query_data=='info':

        try:
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

            last_pull = get_last_git_pull()
            bot.sendMessage(chat_id,"Last Git pull:")
            bot.sendMessage(chat_id,last_pull)
        except Exception as e:
            bot.sendMessage(chat_id,"ERROR INFO:"+ str(e))








    elif query_data=='open1':
        try:
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
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR GATE:" + str(e))



    elif query_data=='open2':
        try:

            print("||_||_ CHECK REBOOT")
            bot.sendMessage(chat_id, "reboot in corso...")
            os.system('sudo reboot')
            now = datetime.now()
            hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
            loggingR.error("(open2)______________________EVENT____________________")
            loggingR.error("APERTURA CANCELLO____time: %s", str(hourstr))
            loggingR.error("UTENTE: %s", str(info))
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR REBOOT:" + str(e))


    elif query_data=='crypto':
        # Send the submenu inline keyboard
        try:
            bot.sendMessage(chat_id, 'CRYPTO:', reply_markup=create_inline_keyboard())
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR CRYPTO MENU:" + str(e))


    elif query_data=='data':

        try:

            invia_immagine(chat_id, FOLDER_GRAPH + "/" + "ALL" + PLOT_STRING_TITLE, bot)
            crypto_string = leggi_stringa_oggi()

            # plot_andamento_cripto(nome_crypto, crypto_portfolio)
            for info in crypto_string:
                info_c = converti_formato_data(info)
                if info_c == "end_simple":
                    break
                else:
                    bot.sendMessage(chat_id,info_c)
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR CRYPTO PORTFOLIO:" + str(e))

    elif query_data == 'update':

        try:

            delete_file(FILEPATH_DATI)
            bot.sendMessage(chat_id, 'distrutto:'+FILEPATH_DATI)
            controlla_file()
            bot.sendMessage(chat_id, "update lanciato")
            #cosi lo distruggo e lo ricreo- forse e troppo difficile calcellare solo l iìultima data. mi serve veramente salvare questi dati?
            #qua inserisci l update
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR CRYPTO UPDATE:" + str(e))

    elif query_data == 'movers':

        try:

            bot.sendMessage(chat_id, 'MOVERS:')
            crypto_string = leggi_stringa_oggi()

            pr = 0
            for info in crypto_string:
                info_c = converti_formato_data(info)
                if info_c == "end_simple":
                    pr = 1
                if pr == 1:
                    bot.sendMessage(chat_id, info_c)


        except Exception as e:
            bot.sendMessage(chat_id, "ERROR CRYPTO MOVERS:" + str(e))



    elif query_data == 'back_to_main_menu':
        try:
            # Send the main menu inline keyboard again
            bot.sendMessage(chat_id, 'Main Menu:', reply_markup=keyboard_1)
        except Exception as e:
            bot.sendMessage(chat_id, "ERROR CRYPTO BACK:" + str(e))




def bot_ini(bot):


    MessageLoop(bot, {'chat': on_chat_message,
      'callback_query': on_callback_query}).run_as_thread()
    print("||_||_ CHECK BOT ONLINE")

    while True:
        sleep(2)



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
crea_file_utenti_autorizzati()


print("||_||_ CHECK BOT")
humidity = 0.0
temperature = 0.0
bot = telepot.Bot('2070265556:AAHtStxZRT_J9hxvBtC7EKdnfM6sXVOgJ4U')

loggingR.error("INI____ALL(4 yeah) PROCs: %s", str(hourstr))
print("||_||_ CHECK PROCESSES")
#p1 = multiprocessing.Process(target=reciver.listen_for_TCP_string, args=(string_from_tcp_ID,))
p2 = multiprocessing.Process(target=bot_ini,args = (bot,))
#p3_ri = multiprocessing.Process(target=reciver.main)
p_sensor = multiprocessing.Process(target=write_data_csv,args = (bot,))


# try:
#     p1.start()
# except Exception as e:
#     loggingR.error("PROCESS error 1:  %s ", e)
try:
    p2.start()
except Exception as e:
    loggingR.error("PROCESS error 2:  %s ", e)
# try:
#     p3_ri.start()
# except Exception as e:
#     loggingR.error("PROCESS error 3:  %s ", e)

try:

    p_sensor.start()
except Exception as e:
    loggingR.error("PROCESS error 4:  %s ", e)
print("||_||_ CHECK START PROCESS")

# print("ID of process p1: {}".format(p1.pid))
print("ID of process p1: {}".format(p2.pid))
# print("ID of process p1: {}".format(p3_ri.pid))
print("ID of process p1: {}".format(p_sensor.pid))

# p1.join()
p2.join()
# p3_ri.join()
p_sensor.join()
