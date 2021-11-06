import Adafruit_DHT
import RPi.GPIO as GPIO
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, KeyboardButton
from telepot.loop import MessageLoop
from time import sleep
import datetime

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                                    [InlineKeyboardButton(text="INFO_CASA",callback_data='info'),
                                     InlineKeyboardButton(text="CANCELLO",callback_data='open1'),
                                     InlineKeyboardButton(text="CANC_ETTO",callback_data='open2')
                                     ]
                                    
                                ]
                            )

    bot.sendMessage(chat_id, "OPZIONI CASA SMART:", reply_markup=keyboard)
 
    print("bot COM succesful")

def on_callback_query(msg):
    query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, chat_id, query_data)
    if query_data=='info':
        now = datetime.datetime.now()
        hourstr = now.strftime("%Y-%m-%d %H:%M:%S")
        hum, temp = Adafruit_DHT.read_retry(sensor, pin)
        bot.sendMessage(chat_id, 'temperature: %s'%temp)
        bot.sendMessage(chat_id, 'humidity: %s'%hum)
        bot.sendMessage(chat_id, str(hourstr))
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

        
        
        
    elif query_data=='open2':
        print("open2")
        bot.sendMessage(chat_id, "apertura cancelletto...")

        

sensor = Adafruit_DHT.DHT11
pin = 4

bot = telepot.Bot('2070265556:AAHtStxZRT_J9hxvBtC7EKdnfM6sXVOgJ4U')
humidity = 0.0
temperature = 0.0

MessageLoop(bot, {'chat': on_chat_message,
      'callback_query': on_callback_query}).run_as_thread()
print("listaning..")
while True:
    sleep(5)
    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            
    
