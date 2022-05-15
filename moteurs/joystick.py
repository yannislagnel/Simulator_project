import utime
import machine
from machine import Pin,PWM, ADC
joystickX = ADC(Pin(27))
joystickY = ADC(Pin(26))
pwmR = PWM(Pin(4))
pwmL = PWM(Pin(5))   
pwmR.freq(1000)
pwmR.duty_u16(0)
pwmL.freq(1000)
pwmL.duty_u16(0)

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
        
        
        


while True:
    moyx=0
    rg=500
    for i in range(rg):
        moyx +=joystickX.read_u16()
    moyx= int(moyx/rg)
    #if moyx>32700 and moyx<38050:
    if moyx<32700:
        pwm=abs(65535-moyx*2)
        if(pwm<2500):
            pwm=2500
        if(pwm>65535 or pwm==(32700*2)):
            pwm=65535
        moteur_run(pwm,0)
    elif moyx>32820:
        pwm=(moyx-32700)*2
        if(pwm<2500):
            pwm=2500
        if(pwm>65535 or pwm==(32700*2)):
            pwm=65535
        moteur_run(pwm,1)
    else:
        moteur_run(0,0)
        

    print("X =",moyx,"Y =",joystickY.read_u16())
    utime.sleep_ms(10)
    