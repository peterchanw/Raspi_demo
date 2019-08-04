#!/usr/bin/env python

import RPi.GPIO as GPIO
import distance
import i2c_lcd1602
import time
import ds18b20
import rgbLed
import PS2Joystick
import touchBtn
import segment

screen = i2c_lcd1602.Screen(bus=1, addr=0x3f, cols=16, rows=2)

def destory():
        GPIO.cleanup()

def loop():
        col = [0,0,0]
        st1 = 0
        st2 = [True,True,True]
        counter = 0
        btnSt = "**"
        while True:
           for st1 in range(0,18):
                tmp = PS2Joystick.getResult()
                status = PS2Joystick.state[tmp]
                col1 = rgbLed.rgbSet(col, st1, st2)
                col = col1[0]
                st1 = col1[1]
                st2 = col1[2]
                screen.cursorTo(0, 0)
                temp = 0
                temp = ds18b20.readTemp(temp)
                screen.println('Temp:' + "{:6}".format(str(temp)) + ' C '+ status)
                print temp
                btnSt = touchBtn.btnStatus(btnSt)
                t = distance.checkdist()
                t = round(t, 1)
                m = '%f' %t
                m = m[:5]
                screen.cursorTo(1, 0)
                screen.println('Dist:' + "{:5}".format(m) + ' cm ' + btnSt)
                print m
                print btnSt
                screen.clear()
                time.sleep(0.1)
                if counter <= 9999:
                    segment.numberDisplay(counter)
                else:
                    counter = 0
                counter += 1
                
if __name__ == '__main__':
        print 'RaspPi project'
        line = "RaspPi project  "
        screen.enable_backlight()
        time.sleep(0.5)
        screen.clear()
        screen.cursorTo(0, 0)
        screen.println(line)
        screen.cursorTo(1, 0)
        line = " " * 16
        screen.println(line)
        time.sleep(0.5)
        screen.enable_backlight()
        screen.clear()
        try:
                distance.setup()
                PS2Joystick.setup()
                touchBtn.setup()
                segment.TM1638_init()
                loop()
        except KeyboardInterrupt:
                destory()
