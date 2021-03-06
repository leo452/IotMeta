from textx import metamodel_from_file
import re
import paho.mqtt.client as mqtt
from vehicle_commands import *
import time
import json
#provide es publish
#request es subscript

class Vehicle:
    def __init__(self, name):
        self.name = name
        self.min_speed_mph = 0
        self.max_speed_mph = 10

    def print_action_with_name_prefix(self, action):
        print("{}: {}".format(self.name, action))

    def turn_on_engine(self):
        self.print_action_with_name_prefix("Turning on the engine")

    def turn_off_engine(self):
        self.print_action_with_name_prefix("Turning off the engine")

    def lock_doors(self):
        self.print_action_with_name_prefix("Locking doors")

    def unlock_doors(self):
        self.print_action_with_name_prefix("Unlocking doors")

    def park(self):
        self.print_action_with_name_prefix("Parking")

    def park_in_safe_place(self):
        self.print_action_with_name_prefix("Parking in safe place")

    def turn_on_headlights(self):
        self.print_action_with_name_prefix("Turning on headlights")

    def turn_off_headlights(self):
        self.print_action_with_name_prefix("Turning off headlights")

    def turn_on_parking_lights(self):
        self.print_action_with_name_prefix("Turning on parking lights")

    def turn_off_parking_lights(self):
        self.print_action_with_name_prefix("Turning off parking lights")

    def accelerate(self):
        self.print_action_with_name_prefix("Accelerating")

    def brake(self):
        self.print_action_with_name_prefix("Braking")

    def rotate_right(self, degrees):
        self.print_action_with_name_prefix("Rotating right {} degrees".format(degrees))

    def rotate_left(self, degrees):
        self.print_action_with_name_prefix("Rotating left {} degrees".format(degrees))

    def set_max_speed(self, mph):
        self.max_speed_mph = mph
        self.print_action_with_name_prefix("Setting maximum speed to {} MPH".format(mph))

    def set_min_speed(self, mph):
        self.min_speed_mph = mph
        self.print_action_with_name_prefix("Setting minimum speed to {} MPH".format(mph))

class VehicleCommandProcessor:
    commands_topic = ""
    processed_commands_topic = ""
    active_instance = None

    def __init__(self, name, vehicle):
        self.name = name
        self.vehicle = vehicle
        VehicleCommandProcessor.commands_topic = \
            "vehicles/{}/commands".format(self.name)
        VehicleCommandProcessor.processed_commands_topic = \
            "vehicles/{}/executedcommands".format(self.name)
        self.client = mqtt.Client(protocol=mqtt.MQTTv311)
        VehicleCommandProcessor.active_instance = self
        self.client.on_connect = VehicleCommandProcessor.on_connect
        self.client.on_message = VehicleCommandProcessor.on_message
        self.client.connect(host="127.0.0.1",
                            port=1883,
                            keepalive=60)

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Result from connect: {}".format(
            mqtt.connack_string(rc)))
        # Check whether the result form connect is the CONNACK_ACCEPTED connack code
        if rc == mqtt.CONNACK_ACCEPTED:
            # Subscribe to the commands topic filter
            client.subscribe(
                VehicleCommandProcessor.commands_topic,
                qos=2)

    @staticmethod
    def on_subscribe(client, userdata, mid, granted_qos):
        print("I've subscribed with QoS: {}".format(
            granted_qos[0]))

    @staticmethod
    def on_message(client, userdata, msg):
        if msg.topic == VehicleCommandProcessor.commands_topic:
            print("Received message payload: {0}".format(str(msg.payload)))
            try:
                message_dictionary = json.loads(msg.payload)
                if COMMAND_KEY in message_dictionary:
                    command = message_dictionary[COMMAND_KEY]
                    vehicle = VehicleCommandProcessor.active_instance.vehicle
                    is_command_executed = False
                    # BOF new code
                    if KEY_MPH in message_dictionary:
                        mph = message_dictionary[KEY_MPH]
                    else:
                        mph = 0
                    if KEY_DEGREES in message_dictionary:
                        degrees = message_dictionary[KEY_DEGREES]
                    else:
                        degrees = 0
                    command_methods_dictionary = {
                        CMD_TURN_ON_ENGINE: lambda: vehicle.turn_on_engine(),
                        CMD_TURN_OFF_ENGINE: lambda: vehicle.turn_off_engine(),
                        CMD_LOCK_DOORS: lambda: vehicle.lock_doors(),
                        CMD_UNLOCK_DOORS: lambda: vehicle.unlock_doors(),
                        CMD_PARK: lambda: vehicle.park(),
                        CMD_PARK_IN_SAFE_PLACE: lambda: vehicle.park_in_safe_place(),
                        CMD_TURN_ON_HEADLIGHTS: lambda: vehicle.turn_on_headlights(),
                        CMD_TURN_OFF_HEADLIGHTS: lambda: vehicle.turn_off_headlights(),
                        CMD_TURN_ON_PARKING_LIGHTS: lambda: vehicle.turn_on_parking_lights(),
                        CMD_TURN_OFF_PARKING_LIGHTS: lambda: vehicle.turn_off_parking_lights(),
                        CMD_ACCELERATE: lambda: vehicle.accelerate(),
                        CMD_BRAKE: lambda: vehicle.brake(),
                        CMD_ROTATE_RIGHT: lambda: vehicle.rotate_right(degrees),
                        CMD_ROTATE_LEFT: lambda: vehicle.rotate_left(degrees),
                        CMD_SET_MIN_SPEED: lambda: vehicle.set_min_speed(mph),
                        CMD_SET_MAX_SPEED: lambda: vehicle.set_max_speed(mph),
                    }
                    if command in command_methods_dictionary:
                        method = command_methods_dictionary[command]
                        # Call the method
                        method()
                        is_command_executed = True
                    if is_command_executed:
                        VehicleCommandProcessor.active_instance.publish_executed_command_message(
                            message_dictionary)
                    else:
                        print("I've received a message with an unsupported command.")
            except ValueError:
                # msg is not a dictionary
                # No JSON object could be decoded
                print("I've received an invalid message.")

    def publish_executed_command_message(self, message):
        response_message = json.dumps({
            SUCCESFULLY_PROCESSED_COMMAND_KEY:
                message[COMMAND_KEY]})
        result = self.client.publish(
            topic=self.__class__.processed_commands_topic,
            payload=response_message)
        return result

    def process_incoming_commands(self):
        self.client.loop()


vehicle_name = "vehiclepi01"
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
            device_name = re.split('/',topic[0])
            nombre = device_name[1]
            vehicle = Vehicle(nombre)
            vehicle_command_processor = VehicleCommandProcessor(nombre, vehicle)
            while True:
                # Process messages and the commands every 1 second
                vehicle_command_processor.process_incoming_commands()
                time.sleep(1)

        else:
            print("llego a otro lado")
            device_name = re.split('/',topic[0])
            nombre = device_name[1]
            vehicle_name = nombre
            commands_topic = "vehicles/{}/commands".format(vehicle_name)
            processed_commands_topic = "vehicles/{}/executedcommands".format(vehicle_name)
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



iot_mm = metamodel_from_file('iot.tx')
iot_model = iot_mm.model_from_file('iot_1.rbt')
iot = Iot()
iot.interpret(iot_model)
