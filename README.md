# IotMeta
# Manual de ejecución del simulador de vehiculo

A continuación se muestran los pasos de ejecución del simulador de vehiculo utilizando el meta lenguaje para los comandos request y provide.

### Contenido

1. Ejecución iot_sim1_subs
2. Ejecución iot_sim_pub_r

### Requerimientos

1. Servidor mosquito instalado host de escucha loopback(127.0.0.1) - puerto de escucha por defecto del servidor 1883
2. Soporte para Python3
3. Soporte para liberia TetxX


### Ejecución iot_sim1_subs


```sh
python iot_sim1_subs

#request('vehicles/hola/commands')
#topic sin comillasvehicles/hola/commands
#['request', "'vehicles/hola/commands')"]
#Se encontro un comando request
#el topico esvehicles/hola/commands
#este es el topico del clientevehicles/hola/commands
#Result from connect: Connection Accepted.
```


### Ejecución iot_sim_pub_r


```sh
python iot_sim_pub_r
#Result from connect: Connection Accepted.
#Subscribed with QoS: 2
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "SET_MAX_SPEED"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "SET_MIN_SPEED"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "LOCK_DOORS"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "TURN_ON_ENGINE"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ROTATE_RIGHT"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ACCELERATE"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ROTATE_RIGHT"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ACCELERATE"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ROTATE_LEFT"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "ACCELERATE"}'
#b'{"SUCCESSFULLY_PROCESSED_COMMAND": "TURN_OFF_ENGINE"}'
```
### Resultados en la interfaz

respuesta en la interfaz de iot_sim1_subs 
```sh
#request('vehicles/hola/commands')
#topic sin comillasvehicles/hola/commands
#['request', "'vehicles/hola/commands')"]
#Se encontro un comando request
#el topico esvehicles/hola/commands
#este es el topico del clientevehicles/hola/commands
#Result from connect: Connection Accepted.
#Received message payload: b'{"CMD": "PARK_IN_SAFE_PLACE"}'
#hola: Parking in safe place
#Received message payload: b'{"CMD": "TURN_OFF_PARKING_LIGHTS"} '
#hola: Turning off parking lights
#Received message payload: b'{"CMD": "SET_MAX_SPEED", "MPH": 30}'
#hola: Setting maximum speed to 30 MPH
#Received message payload: b'{"CMD": "SET_MIN_SPEED", "MPH": 8}'
#hola: Setting minimum speed to 8 MPH
#Received message payload: b'{"CMD": "LOCK_DOORS"}'
#hola: Locking doors
#Received message payload: b'{"CMD": "TURN_ON_ENGINE"}'
#hola: Turning on the engine
#Received message payload: b'{"CMD": "ROTATE_RIGHT", "DEGREES": 15}'
#hola: Rotating right 15 degrees
#Received message payload: b'{"CMD": "ACCELERATE"}'
#hola: Accelerating
#Received message payload: b'{"CMD": "ROTATE_RIGHT", "DEGREES": 25}'
#hola: Rotating right 25 degrees
#Received message payload: b'{"CMD": "ACCELERATE"}'
#hola: Accelerating
#Received message payload: b'{"CMD": "ROTATE_LEFT", "DEGREES": 15}'
#hola: Rotating left 15 degrees
#Received message payload: b'{"CMD": "ACCELERATE"}'
#hola: Accelerating
#Received message payload: b'{"CMD": "TURN_OFF_ENGINE"}'
#hola: Turning off the engine
```
