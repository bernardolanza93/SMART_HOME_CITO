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



# Our "on message" event


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
        hum = float(0)
        temp = float(0)
        hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        print("read : ",hum,temp)
        now = datetime.now()
        current_time = now.strftime('%Y-%m-%d %H:%M:%S')
        
           
        #print("data",t,C,H)
        
        f = open('temp_dataRPCITO.csv', 'a')
        writer = csv.writer(f)
        print("read complete : ",current_time,temp,hum)
        writer.writerow([current_time,temp,hum])
        f.close()
        make_graph()
        time.sleep(60)
        
        
        







#plt.show()



# when connecting to mqtt do this;
# receive messages on this topic

    
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="INFO_CASA",callback_data='info'),
                                     InlineKeyboardButton(text="CANCELLO",callback_data='open1'),
                                     InlineKeyboardButton(text="REBOOT",callback_data='open2')
                                     ]
                                    
                                ]
                            )

    bot.sendMessage(chat_id, "OPZIONI CASA SMART:", reply_markup=keyboard)
 
    print("bot COM succesful")

def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    file_path = '/home/pi/plot_data_citofono.png'
    file_path1 = '/home/pi/plot_rec.png'
    if query_data=='info':
        now = datetime.now()
        hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
        cpu = CPUTemperature()
        bot.sendMessage(chat_id, 'CPU_temp citofono: %s'%str(cpu.temperature))
        bot.sendMessage(chat_id, str(hourstr))
        bot.sendDocument(id, open(path + "RPI", 'rb'))
        print("bot COM succesful")

    elif query_data=='open1':
        print("open1")
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.OUT)
        GPIO.output(3, GPIO.HIGH)
        GPIO.output(3, GPIO.LOW)
        sleep(1)
        GPIO.output(3, GPIO.HIGH)
        bot.sendMessage(chat_id, "apertura cancello...")
        bot.sendMessage(chat_id, "OPZIONI CASA SMART:", reply_markup=keyboard)


        
        
        
    elif query_data=='open2':
        print("open2")
        bot.sendMessage(chat_id, "reboot in corso...")
        os.system('sudo reboot')
        


def bot_ini(bot):
    
    MessageLoop(bot, {'chat': on_chat_message,
      'callback_query': on_callback_query}).run_as_thread()
    print("listaning... bot online")
    while True:
        sleep(1)
        now = datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
    




check_folder("/data/")
try:
    loggingR = logging.getLogger('RPI')
    loggingR.setLevel(logging.INFO)
    fh = logging.FileHandler('./data/RPI.log')
    fh.setLevel(logging.DEBUG)
    loggingR.addHandler(fh)
    loggingR.error("STARDED LOGGING FILE____time: ", datetime.now())
except Exception as e:
    print("ERROR LOGGING: ", e)


sensor = Adafruit_DHT.DHT11
pin = 4




humidity = 0.0
temperature = 0.0
bot = telepot.Bot('2070265556:AAHtStxZRT_J9hxvBtC7EKdnfM6sXVOgJ4U')





print("inizializing process 1")

p1 = multiprocessing.Process(target=reciver.listen_for_TCP_string, args=(string_from_tcp_ID,))
p2 = multiprocessing.Process(target=bot_ini,args = (bot,))
p3_ri = multiprocessing.Process(target=reciver.main)
p_sensor = multiprocessing.Process(target=write_data_csv)
p1.start()
p2.start()
p3_ri.start()
p_sensor.start()


print("ID of process p1: {}".format(p1.pid))
print("ID of process p1: {}".format(p2.pid))
print("ID of process p1: {}".format(p3_ri.pid))
print("ID of process p1: {}".format(p_sensor))

p1.join()
p2.join()
p3_ri.join()
p_sensor.join()
