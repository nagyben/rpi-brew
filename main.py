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

logging_enabled = False

def loop():
    for sensor in sensors:
        sensor.update()

    if (logging_enabled):
        log_data(
            sensors[0].tempC,
            sensors[1].tempC,
            sensors[2].tempC,
            mode
        )

    # Restart loop
    t = Timer(1, loop)
    t.start()

loop()

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
        "logEnabled": logging_enabled,
        "sensors": tempsensors
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
    log.info(sensors)
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

@app.route("/log/<status>", methods=['POST'])
def set_logging(status):
    global logging_enabled
    if status.lower() == "yes" or status == "1" or status.lower() == "true":
        log.info("Client requested logging ON")
        logging_enabled = True
        return jsonify({"message": "Logging enabled"})
    elif status.lower() == "no" or status == "0" or status.lower() == "false":
        log.info("Client requested logging OFF")
        logging_enabled = False
        return jsonify({"message": "Logging disabled"})
    else:
        log.info("Unknown control request")
        return jsonify({"message": "Unknown logging request '{}'".format(status)})