from flask import Flask, render_template, Response
import flask
import socket
import cv2, time

app = Flask('hello')
def gen_frames_camera(camera_num):  
    camera = cv2.VideoCapture(camera_num)  # CAP_DSHOW because of https://answers.opencv.org/question/234933/opencv-440modulesvideoiosrccap_msmfcpp-682-cvcapture_msmfinitstream-failed-to-set-mediatype-stream-0-640x480-30-mfvideoformat_rgb24unsupported-media/
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames_drone():
    tello_video = cv2.VideoCapture("udp://@0.0.0.0:11111")
    while True:
        try:
            ret, frame = tello_video.read()

            if ret:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        except Exception as err:
            print(err)
            tello_video.release()
        
            # sock.sendto("ccw 22.5".encode(), tello_address)
            # response = sock.recv(1024).decode()
            # print("response #4", response)
            # time.sleep(0.5)



@app.route('/video_feed_0')
def video_feed_0():
    return Response(gen_frames_camera(0), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_1')
def video_feed_1():
    return Response(gen_frames_camera(2), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_2')
def video_feed_2():
    return Response(gen_frames_camera(6), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_drone')
def video_feed_drone():
    return Response(gen_frames_drone(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return flask.render_template('./index.html')
app.run()