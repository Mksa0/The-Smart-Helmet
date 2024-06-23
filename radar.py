from gpiozero import PWMLED
from adafruit_rplidar import RPLidar
from adafruit_rplidar import RPLidarException
vibf = PWMLED(18)
vibr = PWMLED(12)
vibl = PWMLED(19)
vibb = PWMLED(13)
vibf.value = 0
vibr.value = 0
vibl.value = 0
vibb.value = 0
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
lidar.connect()
while True:
    try:
    #    print(lidar.get_info())
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                print(distance)
                print(type(distance))

                if angle in range(0 ,90) and distance < 400:
                    print('becarful f r')
                    vibf.value = 0.5
                    vibr.value = 0.5
                    vibl.value = 0
                    vibb.value = 0

                if angle in range(90 ,180) and distance < 400:
                    print('becarful b r')
                    vibf.value = 0
                    vibr.value = 0.5
                    vibl.value = 0
                    vibb.value = 0.5

                if angle in range(180 ,270) and distance < 400:
                    print('becarful b l')
                    vibf.value = 0
                    vibr.value = 0
                    vibl.value = 0.5
                    vibb.value = 0.5

                if angle in range(270 ,360) and distance < 400:
                    print('becarful f l')
                    vibf.value = 0.5
                    vibr.value = 0
                    vibl.value = 0.5
                    vibb.value = 0
                if distance > 500:
                    vibf.value = 0
                    vibr.value = 0
                    vibl.value = 0
                    vibb.value = 0


    except RPLidarException:
        lidar.clear_input()



lidar.stop()
lidar.disconnect()
