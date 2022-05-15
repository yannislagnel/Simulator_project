import utime
import machine
from machine import Pin, PWM

pwmR = PWM(Pin(4))
pwmL = PWM(Pin(5))
pwmR.freq(1000)
pwmR.duty_u16(0)
pwmL.freq(1000)
pwmL.duty_u16(0)

for i in range(0,65535,1000): 
    pwmL.duty_u16(0) #Clock Wise
    pwmR.duty_u16(i)
    utime.sleep_ms(500)
    
for i in range(0,65535,1000):
    pwmR.duty_u16(0) #Anti Clock Wise
    pwmL.duty_u16(i)
    utime.sleep_ms(500)

pwmL.duty_u16(0)
pwmR.duty_u16(0)

button = Pin(15, Pin.IN, Pin.PULL_UP)

while True :
    print(button.value())
    utime.sleep(0.5)
    