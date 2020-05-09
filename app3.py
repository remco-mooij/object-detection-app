import os
from flask import Flask, flash, request, redirect, url_for, render_template, session, jsonify, Response
from werkzeug.utils import secure_filename
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from camera import VideoCamera

import time
from absl import app, logging
import cv2
import numpy as np
import tensorflow as tf
from yolov3_tf2.models import (
    YoloV3, YoloV3Tiny
)
from yolov3_tf2.dataset import transform_images, load_tfrecord_dataset
from yolov3_tf2.utils import draw_outputs
from flask import Flask, request, Response, jsonify, send_from_directory, abort
import os

# customize your API through the following parameters
classes_path = './data/labels/coco.names'
weights_path = './weights/yolov3.tf'
tiny = False                    # set to True if using a Yolov3 Tiny model
size = 416                      # size images are resized to for model
# path to output folder where images with detections are saved
output_path = 'static/detections/'
num_classes = 80                # number of classes in model

allowable_items = ['bicycle', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase',
                   'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racketbottle', 'wine glass', 'cup',
                   'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot',
                   'hot dog', 'pizza', 'donut', 'cakechair', 'sofa', 'pottedplant', 'bed', 'diningtable', 'toilet',
                   'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
                   'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
# load in weights and classes
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

if tiny:
    yolo = YoloV3Tiny(classes=num_classes)
else:
    yolo = YoloV3(classes=num_classes)

yolo.load_weights(weights_path).expect_partial()
print('weights loaded')

class_names = [c.strip() for c in open(classes_path).readlines()]
print('classes loaded')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
upload = os.getcwd() + '/uploads/'

app = Flask(__name__)
dropzone = Dropzone(app)

video_camera = None
global_frame = None

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, video/*'
app.config['DROPZONE_MAX_FILE_SIZE'] = 100
#app.config['DROPZONE_REDIRECT_VIEW'] = 'index'

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'

photos = UploadSet('photos', IMAGES)
# videos = UploadSet('media', default_dest=lambda app: app.instance_root)
# videos = UploadSet('media', VIDEOS)
configure_uploads(app, photos)
patch_request_class(app)  # set maximum file size, default is 16MB

# #Remove files in uploads directory
# filelist = [f for f in os.listdir(upload)]
# [os.remove(os.path.join(upload, f)) for f in filelist]


@app.route('/', methods=['GET', 'POST'])
def index():
	# set session for image results
	if "file_urls" not in session:
		session['file_urls'] = []
	# list to hold our uploaded image urls
	file_urls = session['file_urls']
	response = " "
	#remove temporary images
    # for name in os.listdir(os.getcwd() + '/uploads'):
    # #     os.remove(name)

	# handle image upload from Dropszone
	if request.method == 'POST':
		file_obj = request.files
		for f in file_obj:
			file = request.files.get(f)
			try:
				# save the file with to our photos folder
				filename = photos.save(
                                    file,
                                    name=file.filename
				)

				# append image urls
				file_urls.append(photos.url(filename))
			except:
				# save the file with to our photos folder
				filename = videos.save(
                                    file,
                                    name=file.filename
				)

				# append image urls
				file_urls.append(videos.url(filename))

		session['file_urls'] = file_urls
	# return dropzone template on GET request
	return render_template('index.html', response=get_detections(), img_response=get_image(), img_filenames=get_filenames())

# API that returns JSON with classes found in images


def get_detections():
    raw_images = []
    images = os.listdir(os.getcwd() + '/uploads')
    image_names = []
    for image in images:
        image_names.append(image)
        image_file = os.getcwd() + '/uploads/' + image
        img_raw = tf.image.decode_image(
            open(image_file, 'rb').read(), channels=3)
        raw_images.append(img_raw)
    num = 0

    # create list for final response
    response = []

    for j in range(len(raw_images)):
        # create list of responses for current image
        responses = []
        raw_img = raw_images[j]
        num += 1
        img = tf.expand_dims(raw_img, 0)
        img = transform_images(img, size)

        t1 = time.time()
        boxes, scores, classes, nums = yolo(img)
        t2 = time.time()
        print('time: {}'.format(t2 - t1))

        print('detections:')
        for i in range(nums[0]):
            print('\t{}, {}, {}'.format(class_names[int(classes[0][i])],
                                        np.array(scores[0][i]),
                                        np.array(boxes[0][i])))
            responses.append({
                "class": class_names[int(classes[0][i])],
                "confidence": float("{0:.2f}".format(np.array(scores[0][i])*100))
            })
        response.append({
            "image": image_names[j],
            "detections": responses
        })
        img = cv2.cvtColor(raw_img.numpy(), cv2.COLOR_RGB2BGR)
        img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
        cv2.imwrite(output_path + 'detection' + str(num) + '.jpg', img)
        print('output saved to: {}'.format(
            output_path + 'detection' + str(num) + '.jpg'))

    #remove temporary images
    # for name in image_names:
    #     os.remove(name)
    try:
        return response[0]
    except FileNotFoundError:
        return " "

# API that returns image with detections on it
# @app.route('/image', methods= ['POST'])


def get_image():
	raw_images = []
	images = os.listdir(os.getcwd() + '/uploads')
	for image in images:
		image_file = os.getcwd() + '/uploads/' + image
		img_raw = tf.image.decode_image(
			open(image_file, 'rb').read(), channels=3)
		img = tf.expand_dims(img_raw, 0)
		img = transform_images(img, size)

	t1 = time.time()
	boxes, scores, classes, nums = yolo(img)
	t2 = time.time()
	print('time: {}'.format(t2 - t1))

	print('detections')
	for i in range(nums[0]):
		print('\t{}, {}, {}'.format(class_names[int(classes[0][i])], np.array(
		    scores[0][i]), np.array(boxes[0][i])))

	img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
	img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
	cv2.imwrite(output_path + 'detection.jpg', img)
	print('out saved to: {}'.format(output_path + 'detection.jpg'))

	# prepare image for response
	_, img_encoded = cv2.imencode('.png', img)
	response = img_encoded.tostring()

	try:
		return Response(response=response, status=200, mimetype='image/png')
	except FileNotFoundError:
		abort(404)


def get_filenames():
	from os import listdir
	from os.path import isfile, join
	import json
	detImages = [f for f in listdir(
	    'static/detections') if isfile(join('static/detections', f))]
	detImages = json.dumps(detImages)
	return detImages

    # img = cv2.cvtColor(img_raw.numpy(), cv2.COLOR_RGB2BGR)
    # img = draw_outputs(img, (boxes, scores, classes, nums), class_names)
    # cv2.imwrite(output_path + 'detection.jpg', img)
    # print('output saved to: {}'.format(output_path + 'detection.jpg'))

    # # prepare image for response
    # _, img_encoded = cv2.imencode('.png', img)
    # response = img_encoded.tostring()

    #remove temporary image
    # os.remove(image_name)

    # try:
    #     return Response(response=response, status=200, mimetype='image/png')
    # except FileNotFoundError:
    #     abort(404)
# @app.route('/show_image')
# def results():
# 	# set the file_urls and remove the session variable
# 	file_urls = session['file_urls']
# 	session.pop('file_urls', None)
# 	return render_template('index.html', file_urls=file_urls)


@app.route('/record_status', methods=['POST'])
def record_status():
	global video_camera
	if video_camera == None:
			video_camera = VideoCamera()

	json = request.get_json()

	status = json['status']

	if status == "true":
			video_camera.start_record()
			return jsonify(result="started")
	else:
			video_camera.stop_record()
			return jsonify(result="stopped")


def video_stream():
    global video_camera
    global global_frame

    if video_camera == None:
        video_camera = VideoCamera()

    while True:
        frame = video_camera.get_frame()

        if frame != None:
            global_frame = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


@app.route('/video_viewer')
def video_viewer():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
