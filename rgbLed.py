#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

       
pins = {'pin_R':36, 'pin_G':38, 'pin_B':40}  # pins is a dict

GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
for i in pins:
    GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
    GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led

p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
p_G = GPIO.PWM(pins['pin_G'], 2000)
p_B = GPIO.PWM(pins['pin_B'], 2000)

p_R.start(100)      # Initial duty Cycle = 100 (leds off)
p_G.start(100)
p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def clamp(value, min_value, max_value):	# define the user-defined ‘clamp’ function
        return min(max_value, max(min_value, value)) 

def setColor(col):   # For example : col = 0x112233

        R_val = col[0]
        G_val = col[1]
        B_val = col[2]

        R_val = map(R_val, 0, 255, 0, 100) # clamp the frequency '0-100'
        G_val = map(G_val, 0, 255, 0, 100) # clamp the frequency '0-100'
        B_val = map(B_val, 0, 255, 0, 100) # clamp the frequency '0-100'

        p_R.ChangeDutyCycle(R_val)     # Change duty cycle
        p_G.ChangeDutyCycle(G_val)
        p_B.ChangeDutyCycle(B_val)

def rgbColor():
    for b in range(0,255,60):
                col[2] = b
                print(col)
                for g in range(0,255,60):
                     col[1] = g
                     print(col)
                     for r in range(0,255,60):
                         col[0] = r
                         print(col) 
                         setColor(col)
                         time.sleep(0.5) 

def rgbSet(led, st1, st2):
    ch = st1 % 18
    r_inc = st2[0]
    g_inc = st2[1]
    b_inc = st2[2]
    if ch < 6:                                # focus on red channel 
       if (led[0] >= 0) and (led[0] < 255) and (r_inc == True):           
          led[0] += 60
          if led[0] > 255:
             r_inc = False
          else:
             r_inc = True
       else:
          led[0] -= 60
          if led[0] < 0:
             r_inc = True
          else:
             r_inc = False
       led[0] = clamp(led[0],0,255)
    if ch >= 6 and ch < 12:                                # focus on green channel   
       if (led[1] >= 0) and (led[1] < 255) and (g_inc == True):        
          led[1] += 60
          if led[1] > 255:
             g_inc = False
          else:
             g_inc = True
       else:
          led[1] -= 60
          if led[1] < 0:
             g_inc = True
          else:
             g_inc = False
       led[1] = clamp(led[0],0,255)             # focus on blue channel
    if ch >= 12 and ch < 18:     
       if (led[2] >= 0) and (led[2] < 255) and (b_inc == True):
          led[2] += 60
          if led[2] > 255:
             b_inc = False
          else:
             b_inc = True
       else:
          led[2] -= 60
          if led[2] < 0:
             b_inc = True
          else:
             b_inc = False
       led[2] = clamp(led[0],0,255)    
    setColor(led)
    time.sleep(0.1)
    st2[0] = r_inc
    st2[1] = g_inc
    st2[2] = b_inc
    return (led, st1, st2)	

