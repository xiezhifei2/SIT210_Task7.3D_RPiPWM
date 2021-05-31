import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#Sei GPIO pin
led = 15
trigger = 23
echo = 24

GPIO.setup(led,GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)

#set pin 15 as PWM, 100 Hz freq
pwm = GPIO.PWM(led,100)
#start at 0%
pwm.start(0)

def distance():
    #set trigger to HIGH
    GPIO.output(trigger,True)
    time.sleep(0.00001)
    #after 0.00001s, set to LOW
    GPIO.output(trigger,False)
    
    start = time.time()
    stop = time.time()
    
    #save start time
    while GPIO.input(echo)==0:
        start = time.time()
    #save stop time
    while GPIO.input(echo)==1:
        stop = time.time()
    
    #time difference start and arrival
    gap = stop-start
    
    #sonic speed is 343000 cm/s, and there are go and back
    #so divided by 2
    dis = (gap*343000)/2
    
    return dis

#looping untill KeyboardInterrupt
try:
    while 1:
        dis = distance()
        #if distance grater than 400, change to 0%
        if (dis>400):
            x = 0
        else:
            #100% is fully on, so when fet closer, x will
            #greater and led will brighter
            x = 100-(dis/4)
        
        pwm.ChangeDutyCycle(x)#change duty cycle
        time.sleep(0.01)
        
        
#break the loop when KeyboardInterrupt (control+c)
except KeyboardInterrupt:
    pwm.stop()#stop pwm
    GPIO.cleanup()#cleanup pins










