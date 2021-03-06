# USAGE
#https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/

# import the necessary packages
from pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
import json

import socketio

global headingV
headingV=999
global yprh
yprh=[0,0,0,0]

import pathlib
p = pathlib.Path(__file__).parent.absolute()

f = open(str(p.parent.parent) + '/config.json')
# parse x:
config = json.load(f)
#print(config['video']['FPS'])
# standard Python

FPS = config['video']['FPS']
screenMargin = config['video']['screenMargin']
videoSource = config['video']['videoSource']
hudColorR = config['video']['hudColorR']
hudColorG = config['video']['hudColorG']
hudColorB = config['video']['hudColorB']
onScreenColorR = config['video']['onScreenColorR']
onScreenColorG = config['video']['onScreenColorG']
onScreenColorB = config['video']['onScreenColorB']
videoWidth = config['video']['videoWidth']
videoHeight = config['video']['videoHeight']
fontSize = config['video']['fontSize']

sio = socketio.Client()
#sio.wait()
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0,resolution=(videoWidth,videoHeight)).start()
time.sleep(2.0)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

def drawYPRH(frame, x, y):
	cv2.putText(frame, str(yprh[3]), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (onScreenColorR, onScreenColorG, onScreenColorB), 1)
	# cv2.putText(frame, str(yprh[2]), (40, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
	# cv2.putText(frame, str(yprh[1]), (80, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
	# cv2.putText(frame, str(yprh[0]), (120, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
	#cv2.rectangle(frame, (70 + x,70 + y), (30 + x,55 + y), (onScreenColorR, onScreenColorG, onScreenColorB), 1)


def drawCrosshair(frame, videoWidth, videoHeight):
	#cv2.line(image, start_point, end_point, color, thickness)
	# note "//" is the int division operator
	# cv2.line(im, (videoWidth // 2 - 20, videoHeight // 2), (videoWidth // 2 - 40, videoHeight // 2), (hudColorR,hudColorG,hudColorB))
	# cv2.line(im, (videoWidth // 2 + 20, videoHeight // 2), (videoWidth // 2 + 40, videoHeight // 2), (hudColorR,hudColorG,hudColorB))
	# cv2.line(im, (videoWidth // 2, videoHeight // 2 - 20), (videoWidth // 2, videoHeight // 2 - 40), (hudColorR,hudColorG,hudColorB))
	# cv2.line(im, (videoWidth // 2, videoHeight // 2 + 20), (videoWidth // 2, videoHeight // 2 + 40), (hudColorR,hudColorG,hudColorB));
	cv2.line(frame, (videoWidth // 2 - 20, videoHeight // 2), (videoWidth // 2 - 40, videoHeight // 2), (hudColorR,hudColorG,hudColorB))
	cv2.line(frame, (videoWidth // 2 + 20, videoHeight // 2), (videoWidth // 2 + 40, videoHeight // 2), (hudColorR,hudColorG,hudColorB))
	cv2.line(frame, (videoWidth // 2, videoHeight // 2 - 20), (videoWidth // 2, videoHeight // 2 - 40), (hudColorR,hudColorG,hudColorB))
	cv2.line(frame, (videoWidth // 2, videoHeight // 2 + 20), (videoWidth // 2, videoHeight // 2 + 40), (hudColorR,hudColorG,hudColorB));


def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def  reduce(val, base):
    return val - (val // base) * base


def drawCompass(im, videoWidth, videoHeight, heading):
	minI = 0
	maxI = 360
	compassRange = maxI-minI
	for i in range(minI, maxI):
		# if i%20==0:
		# 	cv2.line(im, (reduce(i+heading,compassRange)+minI, - screenMargin), (reduce(i+heading,compassRange)+minI, + screenMargin + 10), (hudColorR,hudColorG,hudColorB))
		# if i%10==0:
		# 	cv2.line(im, (reduce(i+heading,compassRange)+minI, - screenMargin), (reduce(i+heading,compassRange)+minI, + screenMargin + 5), (hudColorR,hudColorG,hudColorB))
		if i%20==0:
			cv2.line(im, ((i+heading)+minI, - screenMargin), ((i+heading)+minI, + screenMargin + 10), (hudColorR,hudColorG,hudColorB))
		if i%10==0:
			cv2.line(im, ((i+heading)+minI, - screenMargin), ((i+heading)+minI, + screenMargin + 5), (hudColorR,hudColorG,hudColorB))
		K = 1
		if (i == K * map(0,0,360,minI, maxI)):
			cv2.putText(im, "N", (reduce(i+heading+videoWidth//2,compassRange)+minI, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (onScreenColorR, onScreenColorG, onScreenColorB))
		if (i == K * map(270,0,360,minI, maxI)):
			cv2.putText(im, "E", (reduce(i+heading+videoWidth//2,compassRange)+minI, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (onScreenColorR, onScreenColorG, onScreenColorB))
		if (i == K * map(180,0,360,minI, maxI)):
			cv2.putText(im, "S", (reduce(i+heading+videoWidth//2,compassRange)+minI, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (onScreenColorR, onScreenColorG, onScreenColorB))
		if (i == K * map(90,0,360,minI, maxI)):
			cv2.putText(im, "W", (reduce(i+heading+videoWidth//2,compassRange)+minI, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.35,  (onScreenColorR, onScreenColorG, onScreenColorB))
        # drawHeading(im, videoWidth, videoHeight, heading);



def detect_motion(frameCount):
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock
	# initialize the motion detector and the total number of frames
	# read thus far
	md = SingleMotionDetector(accumWeight=0.1)
	total = 0
	lineSpace = 30
	# loop over frames from the video stream
	while True:
		start_time = time.time()
		# read the next frame from the video stream, resize it,
		# convert the frame to grayscale, and blur it
		frame = vs.read()
		frame = imutils.resize(frame, height=videoWidth, width=videoHeight)
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#gray = cv2.GaussianBlur(gray, (7, 7), 0)

		# grab the current timestamp and draw it on the frame
		timestamp = datetime.datetime.now()
		#cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		#Framerate
		cv2.putText(frame, str(int(1.0/(time.time()-start_time))), (screenMargin, frame.shape[0] - lineSpace), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
		#Resolution
		cv2.putText(frame, str(frame.shape[0]), (frame.shape[1] - 80, frame.shape[0] - lineSpace), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
		cv2.putText(frame, "x", (frame.shape[1] - 65, frame.shape[1] - lineSpace), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
		cv2.putText(frame, str(frame.shape[1]), (frame.shape[1] - 50, frame.shape[0] - lineSpace), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 0), 1)
		drawYPRH(frame, screenMargin, 2 * lineSpace)
		#cv2.putText(frame, str(yprh[3]), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (onScreenColorR, onScreenColorG, onScreenColorB), 1)

		drawCrosshair(frame, frame.shape[1], frame.shape[0])
		#drawCompass(frame, frame.shape[1], frame.shape[0], int(round(float(yprh[3]))))
		drawCompass(frame, frame.shape[1], frame.shape[0], int(round(float(yprh[3]))))
		# if the total number of frames has reached a sufficient
		# number to construct a reasonable background model, then
		# continue to process the frame
		#if total > frameCount:
			# detect motion in the image
		#	motion = md.detect(gray)

			# cehck to see if motion was found in the frame
		#	if motion is not None:
				# unpack the tuple and draw the box surrounding the
				# "motion area" on the output frame
		#		(thresh, (minX, minY, maxX, maxY)) = motion
		#		cv2.rectangle(frame, (minX, minY), (maxX, maxY),
		#			(0, 0, 255), 2)

		# update the background model and increment the total number
		# of frames read thus far
		#md.update(gray)
		total += 1

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@sio.on('yprh')
def print_data(*YPRH):
		#print(str(yprh))
		global yprh
		yprh = YPRH
		global headingV
		headingV = yprh[3]
		#print(yprh[3])


sio.connect('http://192.168.1.50:54321')


	# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start a thread that will perform motion detection
	t = threading.Thread(target=detect_motion, args=(
		args["frame_count"],))
	t.daemon = True
	t.start()
	# start the flask app
	app.run(host=args["ip"], port=config['video']['port'], debug=True,
		threaded=True, use_reloader=False)


# release the video stream pointer
vs.stop()
