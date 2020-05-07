import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(32, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

door = GPIO.PWM(12,50)
arm = GPIO.PWM(16,50)
alligator = GPIO.PWM(32,50)

door.start(7.5) #door starts closed
arm.start(12.5) #arm starts inside the box
alligator.start(2.5) #alligator starts facing the back

def default_action:
  if GPIO.input(10) == 1:
    print("switched on")
    door.ChangeDutyCycle(2.5) #open door
    time.sleep(0.5)
    alligator.ChangeDutyCycle(12.5) #turn alligator head to front
    time.sleep(2)
    arm.ChangeDutyCycle(2.5) #move arm out to close switch
    time.sleep(0.5)
  else:
    print("switched off")
    arm.ChangeDutyCycle(12.5) #move arm back in
    time.sleep(0.5)
    alligator.ChangeDutyCycle(2.5) #turn alligator head back
    time.sleep(0.5)
    door.ChangeDutyCycle(7.5) #close door


def switch_activated(channel):
    time.sleep(0.005)
    default_action()


GPIO.add_event_detect(10, GPIO.BOTH, callback=switch_activated, bouncetime=20)

try:
   while True:
      print("waiting for switch")

except KeyboardInterrupt:
   door.ChangeDutyCycle(7.5)
   door.stop()
   arm.ChangeDutyCycle(12.5)
   arm.stop()
   alligator.ChangeDutyCycle(2.5)
   alligator.stop()
   GPIO.remove_event_detect(10)
   GPIO.cleanup()
