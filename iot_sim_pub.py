from textx import metamodel_from_file
import re
import paho.mqtt.client as mqtt
#provide es publish
#request es subscript

vehicle_name = "hola"
commands_topic = "vehicles/{}/commands".format(vehicle_name)
processed_commands_topic = "vehicles/{}/executedcommands".format(vehicle_name)


class LoopControl:
    is_last_command_processed = False


def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(
        mqtt.connack_string(rc)))
    # Check whether the result form connect is the CONNACK_ACCEPTED connack code
    if rc == mqtt.CONNACK_ACCEPTED:
        # Subscribe to the commands topic filter
        client.subscribe(
            processed_commands_topic,
            qos=2)


def on_message(client, userdata, msg):
    if msg.topic == processed_commands_topic:
        print(str(msg.payload))
        if str(msg.payload).count(CMD_TURN_OFF_ENGINE) > 0:
            LoopControl.is_last_command_processed = True


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed with QoS: {}".format(granted_qos[0]))


def build_command_message(command_name, key="", value=""):
    if key:
        # The command requires a key
        command_message = json.dumps({
            COMMAND_KEY: command_name,
            key: value})
    else:
        # The command doesn't require a key
        command_message = json.dumps({
            COMMAND_KEY: command_name})
    return command_message

def publish_command(client, command_name, key="", value=""):
    command_message = build_command_message(
        command_name, key, value)
    result = client.publish(topic=commands_topic,
                            payload=command_message, qos=2)
    time.sleep(1)
    return result


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
            client = mqtt.Client(protocol=mqtt.MQTTv311)
            client.on_connect = on_connect
            client.on_subscribe = on_subscribe
            client.on_message = on_message
            # Set a will to be sent to the MQTT server in case the client
            # disconnects unexpectedly
            last_will_payload = build_command_message(CMD_PARK_IN_SAFE_PLACE)
            client.will_set(topic=commands_topic,
                payload=last_will_payload,
                qos=2,
                retain=True)
            client.connect(host="127.0.0.1",
                            port=1883,
                            keepalive=60)
            client.loop_start()
            publish_command(client, CMD_SET_MAX_SPEED, KEY_MPH, 30)
            publish_command(client, CMD_SET_MIN_SPEED, KEY_MPH, 8)
            publish_command(client, CMD_LOCK_DOORS)
            publish_command(client, CMD_TURN_ON_ENGINE)
            publish_command(client, CMD_ROTATE_RIGHT, KEY_DEGREES, 15)
            publish_command(client, CMD_ACCELERATE)
            publish_command(client, CMD_ROTATE_RIGHT, KEY_DEGREES, 25)
            publish_command(client, CMD_ACCELERATE)
            publish_command(client, CMD_ROTATE_LEFT, KEY_DEGREES, 15)
            publish_command(client, CMD_ACCELERATE)
            publish_command(client, CMD_TURN_OFF_ENGINE)
            while LoopControl.is_last_command_processed == False:
                # Check whether the last command has been processed or not
                # every 500 milliseconds
                time.sleep(0.5)
            client.disconnect()
            client.loop_stop()
            print("llego a otro lado")


iot_mm = metamodel_from_file('iot.tx')
iot_model = iot_mm.model_from_file('iot_1_r.rbt')
iot = Iot()
iot.interpret(iot_model)
