from controller import create_app
from controller.utils.Mysql import Mysql
# from controller.utils.controlmp import ControlMotor
# from controller.utils.Face import Face
# import RPi.GPIO as GPIO
import time

# 创建APP对象
app = create_app('dev')
def tydetect(channel):    
    face = Face()
    mysql = Mysql()
    face_name,facepath = controlmp.camera_pi()
    face_token = face.detect(facepath)
    if face_token:
        confidence,user_id = face.search(face_token)
        controlmp.ocdoor(confidence)
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        mysql.insert(date_time,face_token,confidence,face_name,user_id)
    else:
        controlmp.been()

if __name__ == '__main__': 
    # controlmp = ControlMotor()
    # GPIO.add_event_detect(10, GPIO.RISING, callback=tydetect,bouncetime=200)
    app.run()

        

