import dweepy
import random
import time
import math
from grovepi import *

from threading import Thread

dht_sensor_port = 7
led = 4
buzzer_pin = 2

sleep_time = 1

pinMode(led, "OUTPUT")
pinMode(buzzer_pin, "OUTPUT")

publisher_state = False
temp_state = False
hum_state = False
led_state = False
buzz_state = False
every_state = False
led_and_buzz_state = False



def listener(publisher, temp, hum, led, buzz, every, led_and_buzz):
    for dweet in dweepy.listen_for_dweets_from("iot2"):
        content = dweet["content"]
        sleep_time = content.get["time", ""]
        should_publish = content["publish"]
        print should_publish
        global temp_state, publisher_state, hum_state, led_state, buzz_state, every_state, led_and_buzz_state
        if should_publish == "true":
            # start the publisher thread
            publisher_state = True
            if not publisher.is_alive():
                publisher = Thread(target=publisher_method_dan)
            publisher.start()
        elif should_publish == "temp":
            # start the publisher thread
            temp_state = True
            if not temp.is_alive():
                temp = Thread(target=temp_method)
            temp.start()
        elif should_publish == "hum":
            # start the publisher thread
            hum_state = True
            if not hum.is_alive():
                hum = Thread(target=hum_method)
            hum.start()
        elif should_publish == "led":
                # start the publisher thread
                led_state = True
                if not led.is_alive():
                    led = Thread(target=led_method)
                led.start()
        elif should_publish == "buzz":
                # start the publisher thread
                buzz_state = True
                if not buzz.is_alive():
                    buzz = Thread(target=buzz_method)
                buzz.start()
        elif should_publish == "every":
                # start the publisher thread
                every_state = True
                if not every.is_alive():
                    every = Thread(target=every_method)
                every.start()
        elif should_publish == "led_and_buzz":
                # start the publisher thread
                led_and_buzz_state = True
                if not led_and_buzz.is_alive():
                    led_and_buzz = Thread(target=led_and_buzz_method)
                led_and_buzz.start()
        else:
            temp_state = False
            publisher_state = False
            hum_state = False
            led_state = False
            buzz_state = False
            every_state = False
            led_and_buzz_state = False
            print "wasn't true"

def publisher_method_dan():
    while publisher_state:
        result = dweepy.dweet_for('raspberryPI', {"temperature": 12, "attention_level": 84.5})
        print result
        time.sleep(5)
    print "publishing ending"

def temp_method():
    while temp_state:
        try:
            [temp, hum] = dht(dht_sensor_port,0) #Get the temperature and humidity from sensor
            if math.isnan(temp):
                temp = 0
            result = dweepy.dweet_for('raspberryPI', {"temperature": temp})
            print result
            time.sleep(5)

        except (IOError, TypeError) as e:
            print "Error"
    print "Temp ending"

def led_and_buzz_method():
    while led_and_buzz_state:
        try:
            digitalWrite(led, 1)
            time.sleep(0.5)
            digitalWrite(buzzer_pin, 0)
            time.sleep(1)
            result = dweepy.dweet_for('raspberryPI', {"LED": 1, "Buzzer": 0})
            print result


            digitalWrite(led, 0)
            time.sleep(0.5)
            digitalWrite(buzzer_pin, 1)
            time.sleep(1)
            result = dweepy.dweet_for('raspberryPI', {"LED": 0, "Buzzer": 1})
            print result

        except KeyboardInterrupt:
            digitalWrite(led,0)
            break

        except (IOError, TypeError) as e:
            print "Error"
    print "led and buzzer end"




def hum_method():
    while hum_state:
        try:
            [temp, hum] = dht(dht_sensor_port,0) #Get the temperature and humidity from sensor
            if math.isnan(hum):
                hum = 0
            result = dweepy.dweet_for('raspberryPI', {"humidity": hum})
            print result
            time.sleep(5)

        except KeyboardInterrupt:
            digitalWrite(led,0)
            break

        except (IOError, TypeError) as e:
            print "Error"
    print "Hum ending"

def led_method():
    while led_state:
        try:

            digitalWrite(led,1)
            result = dweepy.dweet_for('raspberryPI', {"LED": 1})
            print result
            time.sleep(5)

            digitalWrite(led,0)
            result = dweepy.dweet_for('raspberryPI', {"LED": 0})
            print result
            time.sleep(5)

        except KeyboardInterrupt:
            digitalWrite(led,0)
            break
        except IOError:
            print "Error"
    print "LED ending"

def buzz_method():
    while buzz_state:
    #return platform.platform()
        try:

            digitalWrite(buzzer_pin,1)
            # print "\tBuzzing"
            result = dweepy.dweet_for('raspberryPI', {"Buzzer": 1})
            print result
            time.sleep(2)


            digitalWrite(buzzer_pin,0)
            result = dweepy.dweet_for('raspberryPI', {"Buzzer": 0})
            print result
            time.sleep(2)

        except KeyboardInterrupt:
            digitalWrite(buzzer_pin,0)
        except (IOError,TypeError) as e:
            print "Error"
    print "Buzz ending"

def every_method():
    while every_state:
    #return platform.platform()
        try:

            digitalWrite(buzzer_pin,1)
            # print "\tBuzzing"
            result = dweepy.dweet_for('raspberryPI', {"Buzzer": 1}, {"LED": 1}, {"humidity": hum}, {"temperature": temp})
            print result
            time.sleep(2)


            digitalWrite(buzzer_pin,0)
            result = dweepy.dweet_for('raspberryPI', {"Buzzer": 0}, {"LED": 0}, {"humidity": hum}, {"temperature": temp})
            print result
            time.sleep(2)

            digitalWrite(led,1)
            result = dweepy.dweet_for('raspberryPI', {"LED": 1})
            print result
            time.sleep(2)

            digitalWrite(led,0)
            result = dweepy.dweet_for('raspberryPI', {"LED": 0})
            print result
            time.sleep(2)

            [temp, hum] = dht(dht_sensor_port,0) #Get the temperature and humidity from sensor
            if math.isnan(hum):
                hum = 0
            result = dweepy.dweet_for('raspberryPI', {"humidity": hum})
            print result
            time.sleep(5)

            [temp, hum] = dht(dht_sensor_port,0) #Get the temperature and humidity from sensor
            if math.isnan(temp):
                temp = 0
            result = dweepy.dweet_for('raspberryPI', {"temperature": temp})
            print result
            time.sleep(5)


        except KeyboardInterrupt:
            digitalWrite(buzzer_pin,0)

        except (IOError,TypeError) as e:
            print "Error"
    print "Buzz ending"



publisher_thread = Thread(target=publisher_method_dan)
temp_thread = Thread(target=temp_method)
hum_thread = Thread(target=hum_method)
led_thread = Thread(target=led_method)
buzz_thread = Thread(target=buzz_method)
every_thread = Thread(target=every_method)
led_and_buzz_thread = Thread(target=led_and_buzz_method)


listener_thread = Thread(target=listener, args=(publisher_thread, temp_thread, hum_thread, led_thread, buzz_thread, every_thread, led_and_buzz_thread,))
listener_thread.start()
