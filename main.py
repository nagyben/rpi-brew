import logging
from tempsensor import TemperatureSensor
# from tempcontrol import TemperatureController
from threading import Timer
import persist
import time
from datalogging import log_data

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
appformatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
consolehandler = logging.StreamHandler()
consolehandler.setFormatter(appformatter)
log.addHandler(consolehandler)

SETTINGS_FILE = 'persist.json'

# ------------------------------------------------------------------------- SETTINGS
persist.load(SETTINGS_FILE)

# ------------------------------------------------------------------------- BREWERY
sensors = [
    TemperatureSensor("red"),
    TemperatureSensor("blue"),
    TemperatureSensor("green")
]

# controller = TemperatureController(control_pin=7, time_period=10)

mode = "IDLE"
prep_start_time = None
boil_start_time = None
mash_start_time = None
ferment_start_time = None


def loop(time_interval):
    for sensor in sensors:
        sensor.update()

    log_data()

    # Restart loop
    t = Timer(time_interval, loop)
    t.start()

# ------------------------------------------------------------------------- FLASK

from flask import Flask, jsonify

log.info("Starting app...")
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
        "sensors": tempsensors
    })

@app.route("/sensor/<name>/<id>/<setpoint>", methods=['POST'])
def create_modify_sensor(name, id, setpoint):
    for sensor in sensors:
        if sensor.name == name:
            log.info("Client requested sensor parameter change")
            sensor.sensor_id = id
            sensor.setpoint_C = setpoint
            log.info(sensors)
            return jsonify({
                "message": "Sensor '{}' updated".format(name),
                "id": id,
                "setpoint": setpoint
            })

    log.info("Client requested sensor creation")
    sensors.append(TemperatureSensor(name, id, setpoint))
    log.info(sensors)
    return jsonify({
        "message": "Sensor '{}' created".format(name),
        "id": id,
        "setpoint": setpoint
    })

@app.route("/prep", methods=['POST'])
def start_prep():
    log.info("Client requested prep start")
    global mode
    mode = "prep"

    global prep_start_time
    prep_start_time = time.time()
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
    return jsonify({"message": "Process stopped"})

@app.route("/control/<status>", methods=['POST'])
def set_control(status):
    if status.lower() == "yes" or status == "1" or status.lower() == "true":
        log.info("Client requested control ON")
        controller.enabled = True
        return jsonify({"message": "Control enabled"})
    elif status.lower() == "no" or status == "0" or status.lower() == "false":
        log.info("Client requested control OFF")
        controller.enabled = False
        return jsonify({"message": "Control disabled"})
    else:
        log.info("Unknown control request")
        return jsonify({"message": "Unknown control request '{}'".format(status)})