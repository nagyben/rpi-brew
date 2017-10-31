import logging
from tempsensor import TemperatureSensor
from tempcontrol import TemperatureController
from threading import Timer
import persist
import time
import datalogging
from datalogging import log_brew_data, log_ferment_data
from flask import Flask, jsonify
import subprocess

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

SETTINGS_FILE = 'persist.json'
SENSOR_UPDATE_INTERVAL = 5

# ------------------------------------------------------------------------- SETTINGS
persist.load(SETTINGS_FILE)

# ------------------------------------------------------------------------- BREWERY
sensors = [
    TemperatureSensor("red"),
    TemperatureSensor("blue"),
    TemperatureSensor("green")
]

controller = TemperatureController(control_pin=11, time_period=10)

mode = "IDLE"
prep_start_time = None
boil_start_time = None
mash_start_time = None
ferment_start_time = None

logging_enabled = False

time_taken = 0
last_sensor_update_time = 0

specific_gravity = list()

# ------------------------------------------------------------------------- FLASK API

app = Flask(__name__)

@app.route("/")
def main():
    return app.send_static_file('home.html')


@app.route("/status")
def get_status():
    log.info("Client requested status")
    tempsensors = []
    for sensor in sensors:
        herp = {
            "name": sensor.name,
            "id": sensor.sensor_id,
            "tempC": sensor.tempC
        }
        tempsensors.append(herp)

    global mode
    return jsonify({
        "mode": mode,
        "prepStartTime": prep_start_time,
        "mashStartTime": mash_start_time,
        "boilStartTime": boil_start_time,
        "fermentStartTime": ferment_start_time,
        "logEnabled": logging_enabled,
        "controlEnabled": controller.enabled,
        "heating": controller.heating,
        "setpoint": controller.setpoint,
        "sensors": tempsensors,
        "performanceMetric": time_taken,
        "specificGravity": specific_gravity
    })


@app.route("/sensor/<name>/<id>", methods=['POST'])
def create_modify_sensor(name, id):
    for sensor in sensors:
        if sensor.name == name:
            log.info("Client requested sensor parameter change")
            sensor.sensor_id = id
            log.info(sensors)
            return jsonify({
                "message": "Sensor '{}' updated".format(name),
                "name": name,
                "id": id
            })

    log.info("Client requested sensor creation")
    sensors.append(TemperatureSensor(name, id))

    update_settings()

    return jsonify({
        "message": "Sensor '{}' created".format(name),
        "name": name,
        "id": id
    })


@app.route("/prep", methods=['POST'])
def start_prep():
    log.info("Client requested prep start")
    global mode
    mode = "prep"

    global prep_start_time
    prep_start_time = time.time()

    update_settings()

    return jsonify({
        "message": "Prep started",
        "prepStartTime": prep_start_time
    })


@app.route("/mash", methods=['POST'])
def start_mash():
    log.info("Client requested mash start")
    global mode
    mode = "mash"

    global mash_start_time
    mash_start_time = time.time()

    update_settings()

    return jsonify({
        "message": "Mash started",
        "mashStartTime": mash_start_time
    })


@app.route("/boil", methods=['POST'])
def start_boil():
    log.info("Client requested boil start")
    global mode
    mode = "boil"

    global boil_start_time
    boil_start_time = time.time()

    update_settings()

    return jsonify({
        "message": "Boil started",
        "boilStartTime": boil_start_time
    })


@app.route("/ferment", methods=['POST'])
def start_ferment():
    log.info("Client requested ferment start")
    global mode
    mode = "ferment"

    global ferment_start_time
    ferment_start_time = time.time()

    update_settings()

    return jsonify({
        "message": "Ferment started",
        "fermentStartTime": ferment_start_time
    })


@app.route("/stop", methods=['POST'])
def stop():
    log.info("Client requested stop")
    global mode
    mode = "idle"

    global prep_start_time, mash_start_time, boil_start_time, ferment_start_time
    prep_start_time = None
    mash_start_time = None
    boil_start_time = None
    ferment_start_time = None

    update_settings()
    return jsonify({"message": "Process stopped"})


@app.route("/control/<status>", methods=['POST'])
def set_control(status):
    if status.lower() == "yes" or status == "1" or status.lower() == "true":
        log.info("Client requested control ON")
        controller.enabled = True
        message = "Control enabled"

    elif status.lower() == "no" or status == "0" or status.lower() == "false":
        log.info("Client requested control OFF")
        controller.enabled = False
        controller.heat_off()
        message = "Control disabled"

    else:
        log.info("Unknown control request")
        message = "Unknown control request '{}'".format(status)

    do_control()
    update_settings()
    return jsonify({"message": message})


@app.route("/log/<status>", methods=['POST'])
def set_logging(status):
    global logging_enabled

    if status.lower() == "yes" or status == "1" or status.lower() == "true":
        log.info("Client requested logging ON")
        logging_enabled = True
        message = "Logging enabled"

    elif status.lower() == "no" or status == "0" or status.lower() == "false":
        log.info("Client requested logging OFF")
        logging_enabled = False
        message = "Logging disabled"

    else:
        log.info("Unknown control request")
        message = "Unknown logging request '{}'".format(status)

    update_settings()
    return jsonify({"message": message})


@app.route("/temp/<temp>", methods=['POST'])
def set_temperature(temp):
    temp = int(temp)
    if temp < 10: temp = 10
    if temp > 30: temp = 30
    controller.setpoint = temp
    update_settings()
    return jsonify({"message": "Temperature set to {}".format(temp)})


@app.route("/force-update", methods=['POST'])
def force_git_update():
    log.info("Requested git update of program")
    message = subprocess.run(["git", "pull"], stdout=subprocess.PIPE).stdout
    message = message.decode("utf-8")
    log.info(message)
    return jsonify({"message": message})


@app.route("/sg/<sg>", methods=['POST'])
def add_gravity(sg):
    sg = int(sg)
    log.info("Request to add gravity reading")
    specific_gravity.append([time.time(), sg])
    if len(specific_gravity) == 1:
        message = "Adding OG {}".format(sg)
    else:
        message = "Adding SG {}".format(sg)
    update_settings()
    return jsonify({"message": message})


@app.route("/sg", methods=['DELETE'])
def delete_gravity():
    log.info("Request to remove last gravity reading")
    if len(specific_gravity) > 0:
        # maybe limit to removing gravity readings in the last hour?
        last_time = specific_gravity[-1][0]
        if time.time() - last_time < 3600:
            specific_gravity.pop()
            message = "Removed last reading"
        else:
            message = "Last reading not removed - over an hour old"
    else:
        message = "Nothing to remove"

    update_settings()
    return jsonify({"message": message})




# ------------------------------------------------------------------------- SETTINGS


def update_settings():
    persist.settings['redId'] = sensors[0].sensor_id
    persist.settings['blueId'] = sensors[1].sensor_id
    persist.settings['greenId'] = sensors[2].sensor_id
    persist.settings['setpointC'] = controller.setpoint
    persist.settings['logEnabled'] = logging_enabled
    persist.settings['controlEnabled'] = controller.enabled
    persist.settings['mode'] = mode
    persist.settings['sg'] = specific_gravity
    persist.settings['fermentStart'] = ferment_start_time
    persist.save(SETTINGS_FILE)


def load_settings():
    if 'redId' in persist.settings:
        sensors[0].sensor_id = persist.settings['redId']

    if 'blueId' in persist.settings:
        sensors[1].sensor_id = persist.settings['blueId']

    if 'greenId' in persist.settings:
        sensors[2].sensor_id = persist.settings['greenId']

    if 'setpointC' in persist.settings:
        controller.setpoint = persist.settings['setpointC']

    if 'logEnabled' in persist.settings:
        global logging_enabled
        logging_enabled = persist.settings['logEnabled']

    if 'controlEnabled' in persist.settings:
        controller.enabled = persist.settings['controlEnabled']

    if 'mode' in persist.settings:
        global mode
        mode = persist.settings['mode']

    if 'log_interval' in persist.settings:
        datalogging.LOG_INTERVAL = persist.settings['log_interval']

    if 'sg' in persist.settings:
        global specific_gravity
        specific_gravity = persist.settings['sg']

    if 'fermentStart' in persist.settings:
        global ferment_start_time
        ferment_start_time = persist.settings['fermentStart']


def update_sensors():
    global last_sensor_update_time
    if time.time() - last_sensor_update_time >= SENSOR_UPDATE_INTERVAL:
        last_sensor_update_time = time.time()
        for sensor in sensors:
            sensor.update()


def do_control():
    if controller.enabled and mode == "ferment":
        controller.control(sensors[0].tempC)
    else:
        controller.enabled = False


def do_logging():
    if logging_enabled:
        if mode.lower() != 'ferment':
            log_brew_data(
                sensors[0].tempC,
                sensors[1].tempC,
                sensors[2].tempC,
                mode
            )
        else:
            log_ferment_data(sensors[0].tempC)


def loop():
    global time_taken
    start_time = time.time()

    update_sensors()
    do_logging()
    do_control()
    update_settings()

    time_taken = (time.time() - start_time) * 1000

    # Restart loop
    t = Timer(1, loop)
    t.start()

# ------------------------------------------------------------------------- START

load_settings() # apply settings

loop() # start loop

