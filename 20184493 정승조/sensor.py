import socket
from threading import Thread
import RPi.GPIO as GPIO
import time
import picamera  

### 나의 IP로 소켓통신 서버 지정 ##

HOST = '172.30.1.32'
PORT = 3008

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()

##### 초음파 인식 촬영 ####

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#led 센서 설정
red_led = 3
green_led = 4
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

# 초음파 센서 설정
ECHO = 23
TRIG = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)


## 현재 주차장에 남은 주차 공간 파악을 위한 변수 ##
#### 초음파 센서 작동 함수 #####
def measure():
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    start = time.time()

    while GPIO.input(ECHO) == 0:
        start = time.time()
    
    while GPIO.input(ECHO) == 1:
        stop = time.time()

    check = stop - start
    distance = check * 34300 / 2
    return distance

def measure_avg():
    dis1 = measure()
    time.sleep(0.1)
    dis2 = measure()
    time.sleep(0.1)
    dis3 = measure()
    distance = (dis1 + dis2 + dis3) / 3
    return distance



def file(data):
    f = open('/home/seungjo/project/park_state.txt', 'w')
    f.write(data)
    f.close()

try:
    count = 0
    while True:
        ### Socekt 통신을 통해 남은 주차 공간 파악 ##
        c_s, addr = s.accept()

        print('Connected By ', addr)
        data = c_s.recv(1024)

        if not data:
            continue

        print('Received data : ', data.decode())
        string = data.decode()
        file(string)
        c_s.close()
        distance = measure_avg()
        print("Distance : %.1f" % distance)
        time.sleep(1)


        # 초음파로 차량의 거리를 측정 후 일정 값에 도달하면
        # 차량의 번호판을 찍고 공유폴더에 저장
        if distance <= 13:
            with picamera.PiCamera() as camera:
                #camera.resolution = (640, 480)
                camera.start_preview()
                time.sleep(0.5)
                camera.capture('/home/seungjo/project/samba/car%d.jpg' %count)
                count += 1
                camera.stop_preview()
                #time.sleep(2.5)
                print("Open")
                GPIO.output(red_led, 0)
                GPIO.output(green_led, 1)
                time.sleep(2.5)
        else:
            print("Close")
            GPIO.output(green_led, 0)
            GPIO.output(red_led, 1)
        
       
except KeyboardInterrupt:
    GPIO.cleanup()
    s.close()
except Exception as ex:
    print("error exception : ",ex)
    GPIO.cleanup()
    s.close()

