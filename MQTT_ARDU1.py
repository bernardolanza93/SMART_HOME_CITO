import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
from time import sleep
from datetime import datetime
import csv
import pandas as pd

#dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S')



headers = ['data','temp','hum']
df = pd.read_csv('temp_dataRPMAN.csv',names=headers)
print (df)

df['data'] = df['data'].map(lambda x: datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S'))
x = df['data']
y = df['temp']
z = df['hum']

'''
# plot
plt.plot(x,y, 'r')
plt.plot(x,z, 'b')
 
# beautify the x-labels
plt.gcf().autofmt_xdate()

#plt.show()
'''

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('time')
ax1.set_ylabel('Temp', color=color)
ax1.plot(x, y, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('hum', color=color)  # we already handled the x-label with ax1
ax2.plot(x,z, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped

plt.savefig('plot.png')

#The simplest way is to start the ntetwork loop on a separate thread using the client.loop_start() function, then use the normal client.publish method


t = ["2022-01-03 16:20:00"]
C = [12]
H = [45]
f = open('temp_dataRPMAN.csv', 'w')
writer = csv.writer(f)






#plt.show()
MQTT_ADDRESS = '192.168.1.90' 
MQTT_USER = 'torre01' 
MQTT_PASSWORD = 'torre' 
MQTT_TOPIC = 'home/+/+'
MQTT_TOPIC_FROM_CITOFONO = 'house/data_citofono'
data_2send_from_mansarda = 'init_mansarda_sender'

 
# when connecting to mqtt do this;
# receive messages on this topic
def on_connect(client, userdata, flags, rc): 
    """ The callback for when the client receives a CONNACK response from the server.""" 
    print('Connected with result code ' + str(rc)) 
    client.subscribe(MQTT_TOPIC)
    print("subscribing to:", MQTT_TOPIC)
    #print("subscribing to:", MQTT_TOPIC_FROM_CITOFONO)
    #client.subscribe(MQTT_TOPIC_FROM_CITOFONO)
def on_connect_2citofono(client, userdata, flags, rc): 
    """ The callback for when the client receives a CONNACK response from the server.""" 
    print('Connected with result code ' + str(rc)) 
    #client.subscribe(MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC_FROM_CITOFONO)

 
# when receiving a mqtt message do this; 
def on_message(client, userdata, message): 
    """The callback for when a PUBLISH message is received from the server.""" 
    message_in = str(message.payload.decode("utf-8"))
    print("rec " ,message_in)
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    #print("Current Time =", current_time)
    
    if message.topic == "home/livingroom/temperature":
       C.append(float(message_in))
       t.append(current_time)
    elif message.topic == "home/livingroom/humidity":
       H.append(float(message_in))
       
    #print("data",t,C,H)
    if len(t) == len(C) and len(C) == len(H):
        
        print("read complete : ",t[-1],C[-1],H[-1])
        writer.writerow([t[-1],C[-1],H[-1]])
        
    
    #plt.savefig('foo.png')
    #print('data :',temp)
def publish_mqtt(data_sent_from_mansarda):#notinuse
    mqttc = mqtt.Client("monto_hub")
    mqttc.connect(Broker, 1883)
    mqttc.publish(pub_topic, "this is the master speaking")
    #mqttc.loop(2) //timeout = 2s    
def main():
    print("crating client to recive ...")
    mqtt_client = mqtt.Client() 
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD) 
    print("on_connecting...")
    mqtt_client.on_connect = on_connect
    print("on_message checking ...")
    
    mqtt_client.on_message = on_message
    
    print("tryng to connect to",MQTT_ADDRESS)
 
    mqtt_client.connect(MQTT_ADDRESS, 1883,60)
    #mqtt_client.publish(pub_topic, "this is the master speaking")#solo se si vuole anche inviare 
    print("connected")
    mqtt_client.loop_forever() 
 
 
if __name__ == '__main__': 
    print('MQTT service Gaiseric') 
    main()
    

