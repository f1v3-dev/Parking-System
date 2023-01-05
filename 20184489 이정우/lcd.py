import drivers
from time import sleep

display = drivers.Lcd()

try:
    while True:
        print("print HelloWorld")

        display.lcd_display_string("Hello World!",1)
        display.lcd_display_string("*WELCOME*",2)
        sleep(2)
        display.lcd_display_string("Hello World!",1)
        display.lcd_display_string("*WELCOME*",2)
        sleep(2)
except KeyboardInterrupt:
    print("Cleaning up!")
    display.lcd_clear()
