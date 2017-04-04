#!/usr/bin/env python3
import time
import json
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Create a dictionary called pins to store the pin number, name, and pin state:
#dict should have been 'Zone X' : {'pin' : XX}, ...
#too far along and too much code change to fix
#realized at json settings
#just going to use 3 vars for pins now
# and pass those to jsonsettings
zone1pin = 17
zone2pin = 27
zone3pin = 22

ipins = {
        zone1pin : {'name' : 'Zone 1', 'state' : GPIO.LOW},
        zone2pin : {'name' : 'Zone 2', 'state' : GPIO.LOW},
        zone3pin : {'name' : 'Zone 3', 'state' : GPIO.LOW}
        }

opins = {
        23 : {'name' : 'Zone 1', 'state' : 'low', 'watches': zone1pin },
        24 : {'name' : 'Zone 2', 'state' : 'low', 'watches': zone2pin },
        25 : {'name' : 'Zone 3', 'state' : 'low', 'watches': zone3pin }
        }

# Set each pin as an output and make it low:
for pin in ipins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in opins:
    GPIO.setup(pin, GPIO.IN)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    global ipins, opins
    ipins = getState() 
    templateData = {
            'pins' : ipins,
            'title' : 'Pawz Sprinkler System'
            }
    return render_template('index.html', **templateData) 

@app.route("/<changePin>/<action>")
def action(changePin, action):
    global ipins, opins
    changePin = int(changePin)
    deviceName = ipins[changePin]['name']
    if action == 'on':
       allOff()
       GPIO.output(changePin, GPIO.HIGH)
       message = 'Turned {0} On'.format(deviceName)
    if action == 'off':
       GPIO.output(changePin, GPIO.LOW)
       message = 'Turned {0} Off'.format(deviceName)

    ipins = getState() 

    templateData = {
        'pins' : ipins,
        'message' : message
    }

    return render_template('index.html', **templateData)

def getState():
    global ipins, opins
    for pin in opins:
        #read pin to ensure state, since I think multiple
        #web pages could control it
        #GPIO input returns True or False
        opins[pin]['state'] = GPIO.input(pin)
        ipins[opins[pin]['watches']]['state'] = opins[pin]['state'] 

    return ipins

def allOff():
    global ipins, opins
    for pin in ipins:
        GPIO.output(pin, GPIO.LOW)

@app.route('/setup')
def setup():
    templateData = {
            'localtime' : time.strftime("%H:%M %Z", time.localtime()),
            'localdate' : time.strftime("%d %b %Y", time.localtime())
                    }
    error = None
    if (request.args):
        f = open('settings.json', 'w')
        f.write(json.dumps(request.args))
        f.close()
        return redirect(url_for('set'))

    return render_template('setup.html', **templateData)

@app.route('/settings')
def set():
    f = open('settings.json', 'r')
    settings = f.read()
    f.close()
    settings = json.loads(settings)
    templateData = {
        'settings' : settings,
    }
    return render_template('settings.html', **templateData)


@app.route('/jsonsettings')
def jsonset():
    global ipins
    f = open('settings.json', 'r')
    settings = f.read()
    f.close()
    settings = json.loads(settings)
    info = {'settings': settings, 'pins': ipins, 'zone1pin': zone1pin, 'zone2pin': zone2pin, 'zone3pin': zone3pin, }
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=False, port=80, host='0.0.0.0')
