#!/usr/bin/env python3
import time
import json
import requests


def main():
    settings = getSettings()
    waterSettings = settings['settings']
    
    print(waterSettings)
    #break if new settings
    while( waterSettings == getSettings()['settings'] ):
        sleep = 30
        now = time.localtime()
        year, mon, day, hour, mins, sec, wday, yday, isdst  = now
        
        #delete - testing
        water_lawn( waterSettings, settings['zone1pin'],
                    settings['zone2pin'], settings['zone3pin'],
                    waterSettings['evening-duration'])
        
        #if the hours and mins match, water the lawn
        if( hour == int( waterSettings['morning-run-start-hour']) and
            mins == int( waterSettings['morning-run-start-min'])):
            water_lawn( waterSettings, settings['zone1pin'],
                        settings['zone2pin'], settings['zone3pin'],
                        waterSettings['morning-duration'])

        if( hour == int( waterSettings['evening-run-start-hour']) and
            mins == int( waterSettings['evening-run-start-min'])):
            water_lawn( waterSettings, settings['zone1pin'],
                        settings['zone2pin'], settings['zone3pin'],
                        waterSettings['evening-duration'])

        #geting close to time, sleep less / poll quicker
        if( mins+1 == int( waterSettings['morning-run-start-min']) or
            mins+1 == int( waterSettings['evening-run-start-min'])):
            sleep = 10
        
        #take a nap
        time.sleep(sleep)


        
def water_lawn(waterSettings, zone1, zone2, zone3, duration):
    if( waterSettings['weather-check'] == 'on' ):
        rain = getRaining();
        if( rain ):
            return

    if( waterSettings['zone1'] == 'on' ):
        req = requests.get('http://127.0.0.1/{0}/on'.format(zone1))
        time.sleep( float(duration)*60)
        req = requests.get('http://127.0.0.1/{0}/off'.format(zone1))

    if( waterSettings['zone2'] == 'on' ):
        req = requests.get('http://127.0.0.1/{0}/on'.format(zone2))
        time.sleep( float(duration)*60)
        req = requests.get('http://127.0.0.1/{0}/off'.format(zone2))

    if( waterSettings['zone3'] == 'on' ):
        req = requests.get('http://127.0.0.1/{0}/on'.format(zone3))
        time.sleep( float(duration)*60)
        req = requests.get('http://127.0.0.1/{0}/off'.format(zone3))

def getRaining():
    #eventually link to open weather api or something
    return False

def getSettings():
    req = requests.get('http://127.0.0.1/jsonsettings')
    return json.loads(req.text)

if __name__ == '__main__':
    main()
