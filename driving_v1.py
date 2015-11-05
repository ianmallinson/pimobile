import sys
import getopt

sys.path.insert(0,'/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
sys.path.append('.')

import RTIMU
import os.path
#import time
import math
#from datetime import datetime
from Adafruit_PWM_Servo_Driver import PWM
#import matplotlib.pyplot as plt
#import numpy as np
import pygame
from pygame.locals import *

#initializing variables
pygame.init()
screen=pygame.display.set_mode((640,480),0,24)
pygame.display.set_caption("Key Press Test")
f1=pygame.font.SysFont("comicsansms",24)

pwm = PWM(0x40)
pwm.setPWMFreq(60)

SETTINGS_FILE = "RTIMULib"


def computeHeight(pressure):
    return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
pressure = RTIMU.RTPressure(s)
humidity = RTIMU.RTHumidity(s)

print("IMU Name: " + imu.IMUName())
print("Pressure Name: " + pressure.pressureName())
print("Humidity Name: " + humidity.humidityName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded");

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

if (not pressure.pressureInit()):
    print("Pressure sensor Init Failed")
else:
    print("Pressure sensor Init Succeeded")

if (not humidity.humidityInit()):
    print("Humidity sensor Init Failed")
else:
    print("Humidity sensor Init Succeeded")

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

#set stopped and centred initially
pwm.setPWM(1,0,400)
pwm.setPWM(0,0,400)

speed=400
steer=400
flag=0
fusionPose=0
name="null"
screen.fill((255,255,255))

#main loop which drives the vehicle
while flag==0:
    for i in pygame.event.get():
        if pygame.key.get_focused():
            press=pygame.key.get_pressed()
            for i in xrange(0,len(press)):
                if press[i]==1:
                    name=pygame.key.name(i)
                    if name=="left":
                        steer -=120
                    elif name=="right":
                        steer +=120
                    elif name=="up":
                        speed +=50
                    elif name=="down":
                        speed -=50
                    elif name=="space":
                        steer=400
                    elif name=="x":
                        speed=400
                    elif name=="escape":
                        flag=1

            pwm.setPWM(0,0,speed)
            pwm.setPWM(1,0,steer)

    if imu.IMURead():
        data = imu.getIMUData()
        fusionPose = data["fusionPose"]

    screen.fill((255,255,255))
    text=f1.render(name,True,(0,0,0))
    screen.blit(text,(100,100))
    text2=f1.render("Steering %s" % str(steer),True,(0,0,0))
    screen.blit(text2,(100,150))
    text3=f1.render("Speed %s" % str(speed),True,(0,0,0))
    screen.blit(text3,(100,200))
    text4=f1.render("Heading %s" % str(int(math.degrees(fusionPose[2]))),True,(0,0,0))
    screen.blit(text4,(100,250))
    pygame.display.update()



#t=datetime.now()
#timu=0
#vel=0

##for loop in range(1,100000):
    #if imu.IMURead():
        #data = imu.getIMUData()
        #fusionPose = data["fusionPose"]
        ##print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
        #deltapi=datetime.now()-t
        ##print("deltapi %f" % deltapi.microseconds)
        #t=datetime.now()
        #deltaimu=data["timestamp"]-timu
        ##print("deltaimu: %f" % deltaimu)
        #timu=data["timestamp"]
        #acc=data["accel"][0]
        #vel=vel+(acc*(deltapi.microseconds))/1000000
        #print(data)
        ##print(vel)




#while True:
#  if imu.IMURead():
#    # x, y, z = imu.getFusionData()
#    # print("%f %f %f" % (x,y,z))
#    data = imu.getIMUData()
#    (data["pressureValid"], data["pressure"], data["pressureTemperatureValid"], data["pressureTemperature"]) = pressure.pressureRead()
#    (data["humidityValid"], data["humidity"], data["humidityTemperatureValid"], data["humidityTemperature"]) = humidity.humidityRead()
#    fusionPose = data["fusionPose"]
#    print("r: %f p: %f y: %f" % (math.degrees(fusionPose[0]),
#        math.degrees(fusionPose[1]), math.degrees(fusionPose[2])))
#    if (data["pressureValid"]):
#        print("Pressure: %f, height above sea level: %f" % (data["pressure"], computeHeight(data["pressure"])))
#    if (data["pressureTemperatureValid"]):
#        print("Pressure temperature: %f" % (data["pressureTemperature"]))
#    if (data["humidityValid"]):
#        print("Humidity: %f" % (data["humidity"]))
#    if (data["humidityTemperatureValid"]):
#        print("Humidity temperature: %f" % (data["humidityTemperature"]))
#    time.sleep(poll_interval*1.0/1000.0)

# Disable PWM outputs
pwm.setPWM(0,4096,0)
pwm.setPWM(1,4096,0)

