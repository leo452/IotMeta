from textx import metamodel_from_file
import re
import paho.mqtt.client as mqtt
#provide es publish
#request es subscript

def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))
    # Subscribe to the vehicles/vehiclepi01/tests topic filter
    #client.subscribe("vehicles/vehiclepi01/tests", qos=2)
    client.subscribe(client.topic, qos=2)

def on_subscribe(client, userdata, mid, granted_qos):
    print("I've subscribed with QoS: {}".format(
        granted_qos[0]))

def on_topic(client, topic):
    client.topic = topic

def on_message(client, userdata, msg):
    print("Message received. Topic: {}. Payload: {} ".format(
        msg.topic,
        str(msg.payload)))

class Iot(object):

  def interpret(self, model):

    # model is an instance of Program
    for c in model.commands:
        print(c)
        #print(c.__class__)
        #print(type(c))
        comand_type = re.split('\(', c)
        topic = re.split('\)',comand_type[1])
        topic[0] = topic[0].replace("'","")
        print("topic sin comillas"+topic[0])
        print(comand_type)
        if comand_type[0] == "request":
            print("Se encontro un comando request")
            print("el topico es"+topic[0])
            client = mqtt.Client(protocol=mqtt.MQTTv311)
            setattr(client, 'topic', topic[0])
            print("este es el topico del cliente"+client.topic)
            #client.topic = topic[0]
            #client.on_topic = on_topic(topic[0])
            client.on_connect = on_connect
            client.on_subscribe = on_subscribe
            client.on_message = on_message
            client.connect(host="127.0.0.1",
                port=1883,
                keepalive=60)
            client.loop_forever()

        else:
            print("llego a otro lado")


iot_mm = metamodel_from_file('iot.tx')
iot_model = iot_mm.model_from_file('iot_1.rbt')
iot = Iot()
iot.interpret(iot_model)
