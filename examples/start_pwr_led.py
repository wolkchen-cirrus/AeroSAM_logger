from gpiozero import LED
import signal


pwr = LED(13)
pwr.on()
signal.pause()
