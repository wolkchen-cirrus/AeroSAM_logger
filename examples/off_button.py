from gpiozero import Button
import os


shdwn = Button(16, bounce_time=0.2)
shdwn.wait_for_press()
print("Shutdown Button Pressed")
os.system("sudo shutdown -h now")
