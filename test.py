import sys
sys.path.insert(0,'/home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_PWM_Servo_Driver')
import time

from Adafruit_PWM_Servo_Driver import PWM
pwm = PWM(0x40)
pwm.setPWMFreq(60)

pwm.setPWM(1,0,400)
pwm.setPWM(0,0,450)
time.sleep(3)
pwm.setPWM(1,0,600)
time.sleep(1.5)
pwm.setPWM(1,0,200)
pwm.setPWM(0,0,350)
time.sleep(3)
pwm.setPWM(0,0,400)
pwm.setPWM(1,0,600)
pwm.setPWM(0,0,450)
time.sleep(2)
pwm.setPWM(1,0,400)
time.sleep(2)
pwm.setPWM(0,0,400)

pwm.setPWM(0,4096,0)
pwm.setPWM(1,4096,0)

print "hello woddrld"
a = 5
print a
for b in range(0, 5):
    print b
    print a
print "donhje"
