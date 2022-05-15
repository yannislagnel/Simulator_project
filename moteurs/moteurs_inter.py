import utime
import machine
from machine import Pin, PWM

encodeurA = Pin(21, Pin.IN, Pin.PULL_UP)
encodeurB = Pin(22, Pin.IN, Pin.PULL_UP)
counter = 0 

pwmR = PWM(Pin(4))
pwmL = PWM(Pin(5))   
pwmR.freq(1000)
pwmR.duty_u16(0)
pwmL.freq(1000)
pwmL.duty_u16(0)


def motRST_IRQ(Pin):
    global counter
    #moteur_run(0,0)
    #print(Pin.value())
    print(counter)
    #utime.sleep_ms(10)
    counter=0
   
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


motRST = Pin(15, Pin.IN, Pin.PULL_UP)
motRST.irq(trigger=Pin.IRQ_RISING,handler=motRST_IRQ)
encodeurA.irq(trigger=Pin.IRQ_FALLING,handler=motENC_IRQ)


moteur_run(20000,1)
utime.sleep(50)
'''
moteur_run(20000,0)
utime.sleep(3)
moteur_run(0,1)
utime.sleep(3)
'''
moteur_run(2500,0)
utime.sleep(5)

moteur_run(2500,1) 

while True :
    #print(motRST.value())
    #print("counter = ", counter)
    utime.sleep(0.5)
    
    