import RPi.GPIO as GPIO
import time


#socket
import socket


# lcd
import drivers
from time import sleep

display = drivers.Lcd() 

#MySql
import MySQLdb

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#connect pin
TRIG_0 = 12
ECHO_0 = 16

TRIG_1 = 23
ECHO_1 = 24

R_LED_0 = 27
G_LED_0 = 22

R_LED_1 = 20
G_LED_1 = 21



#check state
Cstate_0 = False
Cstate_1 = False

#init count
ParkedCount = 0
EmptyCount = 2

#sensor
GPIO.setup(TRIG_0,GPIO.OUT)
GPIO.setup(ECHO_0,GPIO.IN)

GPIO.setup(TRIG_1,GPIO.OUT)
GPIO.setup(ECHO_1,GPIO.IN)

#led
GPIO.setup(R_LED_0,GPIO.OUT)
GPIO.setup(G_LED_0,GPIO.OUT)

GPIO.setup(R_LED_1,GPIO.OUT)
GPIO.setup(G_LED_1,GPIO.OUT)


GPIO.output(TRIG_0,False)
time.sleep(2)
GPIO.output(TRIG_1,False)
time.sleep(2)

def file_search(arr_number,arr_date):
    f = open("/home/jeongwoo/sambashare/number.txt",'r')
    while True:
        line = f.readline()
        if not line:
            f.close()
            break
        number_d = line[0:8]
        date_d = line[8:-1]

        arr_number.append(number_d)
        arr_date.append(date_d)



def message():
        #socket connect
        
        HOST = '172.30.1.32'
        PORT = 3008
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))

        state1 = str(Cstate_0)
        state2 = str(Cstate_1)
        state = state1+','+state2
        message = state.encode()
        s.sendall(message)
        s.close()
try:

    #HOST = '172.30.1.33'
    #PORT = 3008

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.bind((HOST,PORT))
    #s.listen()
    #connection, addr = s.accept()
    
    while True:


        # sensor 0
        GPIO.output(TRIG_0,True)
        time.sleep(0.00001)
        GPIO.output(TRIG_0,False)

        while GPIO.input(ECHO_0)== 0:
            start_0 = time.time()

        while GPIO.input(ECHO_0) == 1:
            stop_0 = time.time()


        check_time_0 = stop_0 - start_0
        distance_0 = check_time_0 * 34300 / 2
        print("Distance_0 : %.1f cm" % distance_0)
        time.sleep(0.3)
        
        if(distance_0 <= 10.0):
            GPIO.output(R_LED_0,1)
            GPIO.output(G_LED_0,0)
            if(Cstate_0 == False):
                Cstate_0 = True
                ParkedCount = ParkedCount + 1
                EmptyCount = EmptyCount - 1


        else:
            GPIO.output(R_LED_0,0)
            GPIO.output(G_LED_0,1)
            if(Cstate_0 == True):
                Cstate_0 = False
                ParkedCount = ParkedCount - 1
                EmptyCount = EmptyCount + 1

                
        time.sleep(0.5)

        # sensor 1
        GPIO.output(TRIG_1,True)
        time.sleep(0.00001)
        GPIO.output(TRIG_1,False)

        while GPIO.input(ECHO_1) == 0:
            start_1 = time.time()

        while GPIO.input(ECHO_1) == 1:
            stop_1 = time.time()


        check_time_1 = stop_1 - start_1
        distance_1 = check_time_1 * 34300 / 2
        print("Distance_1 : %.1f cm" % distance_1)
        time.sleep(0.3)

        if(distance_1 <= 10.0):
            GPIO.output(R_LED_1,1)
            GPIO.output(G_LED_1,0)
            if(Cstate_1 == False):
                Cstate_1 = True
                ParkedCount = ParkedCount + 1
                EmptyCount = EmptyCount - 1



        else:
            GPIO.output(R_LED_1,0)
            GPIO.output(G_LED_1,1)
            if(Cstate_1 == True):
                Cstate_1 = False
                ParkedCount = ParkedCount - 1
                EmptyCount = EmptyCount + 1

        time.sleep(0.5)

        
        # read sql
        count_info = 0
        db = MySQLdb.connect("localhost","pi","1234","test")
        cur = db.cursor()
        count_info = cur.execute("select car_number from numberCheck;")

        number_data = []
        date_data = []
        # read_file date
        file_search(number_data,date_data)
        print(count_info)
        print(len(number_data))
        if(count_info < len(number_data)):
            for i in range(count_info,len(number_data)):
                try:
                    cur.execute("insert into numberCheck values('"+
                                date_data[i]+"','"+number_data[i] + "')")
                    cur.execute("commit")
                except Exception as ex:
                    print('error exception2 : ',ex)
        else:
            print("not new data")
        

            
        time.sleep(2)
        
        # lcd
        display. lcd_display_string("EmptyCount : "+str(EmptyCount),1)
        display.lcd_display_string("Parked : "+ str(ParkedCount),2)

        message()

except KeyboardInterrupt:
    print("Error")
    s.close()
    cur.close()
    db.close()
    GPIO.cleanup()
    display.lcd_clear()
except Exception as ex:
    print('error exception_main : ',ex)
    s.close()
    cur.close()
    db.close()
    GPIO.cleanup()
    display.lcd_clear()



