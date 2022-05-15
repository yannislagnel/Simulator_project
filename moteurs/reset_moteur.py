import utime
import machine
from machine import Pin, PWM
import random

encodeurA = Pin(21, Pin.IN, Pin.PULL_UP)
encodeurB = Pin(22, Pin.IN, Pin.PULL_UP)
counter = 0 
isreset=False

pwmR = PWM(Pin(4))
pwmL = PWM(Pin(5))   
pwmR.freq(1000)
pwmR.duty_u16(0)
pwmL.freq(1000)
pwmL.duty_u16(0)


def motRST_IRQ(Pin):
    #print(Pin.value())
    global counter,isreset
    utime.sleep_ms(100)
    counter=0
    isreset=True
    
    
    
def motENC_IRQ(Pin):
    global counter
    if encodeurB.value() == 1:
        counter +=1
    else:
        counter -=1
    #print (counter)
        
 
def moteur_run(speed, sens):
    #sens = 1 forward et 0 reverse.
    #speed = 0 arret 65535 Duty Cycle de 1.
    if(speed<=0):
         pwmL.duty_u16(0) #Clock Wise
         pwmR.duty_u16(0)
    elif(sens==1):
        pwmL.duty_u16(0) #Clock Wise
        pwmR.duty_u16(speed)
    else:
        pwmR.duty_u16(0) #Anti Clock Wise
        pwmL.duty_u16(speed)

 #do reset moteur
def resetmoteur():
    global isreset 
    moteur_run(3000,0)
    while isreset==False:
        utime.sleep_us(500)
    moteur_run(0,0)
    counter=0
    isreset=False
    
def move(setpoint):
    if setpoint == counter:
        moteur_run(0, 0)
    elif setpoint > counter:
        moteur_run(30000, 1)
        while counter <= setpoint:
            utime.sleep_us(10)
        moteur_run(0, 0)
    else:
        moteur_run(30000, 0)
        while counter >= setpoint:
            utime.sleep_us(10)
        moteur_run(0, 0)
    #print("You reached your destination:", counter)

######################### MAIN #########################

    
motRST = Pin(15, Pin.IN, Pin.PULL_UP)
motRST.irq(trigger=Pin.IRQ_RISING,handler=motRST_IRQ)
encodeurA.irq(trigger=Pin.IRQ_FALLING,handler=motENC_IRQ)
resetmoteur()
move(600)

while True:
    setpoint=random.randint(10,1600)
    move(setpoint)
    print("You reached your destination:",setpoint," counter=" , counter)
    utime.sleep_ms(100)



###### move to 800
moteur_run(3000,1)
while counter< 810:
    utime.sleep_ms(1)
moteur_run(0,0)
print(counter)
utime.sleep(2)

###### move to 1200
moteur_run(3000,1)
while counter< 1200:
    utime.sleep_ms(1)
moteur_run(0,0)
print(counter)
utime.sleep(2)

###### move to 400
moteur_run(3000,0)
while counter> 400:
    utime.sleep_ms(1)
moteur_run(0,0)
print(counter)
utime.sleep(2)



while True :
    #print(motRST.value())
    #print("counter = ", counter)
    utime.sleep(0.5)
    
    