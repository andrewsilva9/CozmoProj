import cv2
import os
import datetime
import numpy as np
import random

# emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Emotion list
emotions = ["neutral", "anger", "happy", "sadness"]  # Emotion list

# emotions = ["anger", "happy", "sadness", "surprise", "neutral"]  # Emotion list
fishface = cv2.face.createFisherFaceRecognizer()  # Initialize fisher face classifier

data = {}


def get_files(emotion):  # Define function to get file list, randomly shuffle it and split 80/20
	files = os.listdir(os.path.join("../CozmoProj/dataset", emotion))
	# file_size = len(files)
	# files = np.array(files)
	# choices = np.random.choice(file_size, file_size, replace=True)
	# training = files[choices]  # get random 100% of file list should be 60% overlap
	training = files[:int(len(files) * 1)]  # get first 80% of file list
	return training


def make_sets():
	training_data = []
	training_labels = []

	for emotion in emotions:
		training = get_files(emotion)
		source_path = os.path.join("../CozmoProj/dataset", emotion)
		# Append data to training and prediction list, and generate labels 0-7
		for item in training:
			if item.startswith('.'):
				continue
			gray = cv2.imread(os.path.join(source_path, item), 0)  # open image
			# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
			training_data.append(gray)  # append image array to training data list
			training_labels.append(emotions.index(emotion))

	return training_data, training_labels


def run_recognizer(num_run=0):
	training_data, training_labels = make_sets()
	time_str = datetime.datetime.now().isoformat()
	print("{}: Training Fisher face classifier".format(time_str))
	print("{}: size of training set is: {} images".format(time_str, len(training_data)))
	fishface.train(training_data, np.asarray(training_labels))
	# fishface.save('fish_models/fish_model' + str(num_run) + '.xml')
	fishface.save('new_model.xml')
	time_str = datetime.datetime.now().isoformat()
	print("{}: Finished Classifier".format(time_str))
	return

run_recognizer()
# Now run it
# for i in range(0, 10):
# 	run_recognizer(num_run=i)
