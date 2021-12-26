import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import time
from time import sleep

#The simplest way is to start the network loop on a separate thread using the client.loop_start() function, then use the normal client.publish method

t = [0,1]
C = [0,1]
H = []
plt.plot(t,C)
#plt.xlabel('ore', color = '#1ebc3')
plt.ylabel('temp C', color = '#e74c3c')
plt.title('temp stanza 1', color = '#34495e')
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
    #client.subscribe(MQTT_TOPIC)
    print("subscribing to:", MQTT_TOPIC_FROM_CITOFONO)
    client.subscribe(MQTT_TOPIC_FROM_CITOFONO)
def on_connect_2citofono(client, userdata, flags, rc): 
    """ The callback for when the client receives a CONNACK response from the server.""" 
    print('Connected with result code ' + str(rc)) 
    #client.subscribe(MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC_FROM_CITOFONO)

 
# when receiving a mqtt message do this; 
def on_message(client, userdata, message): 
    """The callback for when a PUBLISH message is received from the server.""" 
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    #print('data :',temp)
def publish_mqtt(data_sent_from_mansarda):#notinuse
    mqttc = mqtt.Client("monto_hub")
    mqttc.connect(Broker, 1883)
    mqttc.publish(pub_topic, "this is the master speaking")
    #mqttc.loop(2) //timeout = 2s    
def main():
    print("crating client to recive ...")
    mqtt_client = mqtt.Client() 
    #mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD) 
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
    

