from djitellopy import Tello
import cv2

me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

print(me.get_battery())

me.streamoff()
me.streamon()

while True:
    frame_read = me.get_frame_read()
    my_frame = frame_read.frame
    ret, buffer = cv2.imencode('.jpg', my_frame)
    frame = buffer
    cv2.imshow("tello", frame)