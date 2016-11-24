from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import cv2
import os
import datetime
import numpy as np
import random

emotions = ["neutral", "anger", "happy", "sadness"]  # Emotion list


def get_files(emotion):  # Define function to get file list, randomly shuffle it and split 80/20
	files = os.listdir(os.path.join("../CozmoProj/dataset", emotion))
	# file_size = len(files)
	# files = np.array(files)
	# choices = np.random.choice(file_size, file_size, replace=True)
	# pred_choices = np.random.choice(file_size, int(file_size * 0.2), replace=False)
	# training = files[choices]  # get random 100% of file list should be 60% overlap
	# prediction = files[pred_choices]  # get random 20% of file list
	# training = files[:]
	# prediction = files[-100:]
	random.shuffle(files)
	training = files[:int(len(files) * 1)]
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
			gray = np.reshape(gray, -1)
			training_data.append(gray)  # append image array to training data list
			training_labels.append(emotions.index(emotion))

	return training_data, training_labels


def run_recognizer():
	training_data, training_labels = make_sets()
	time_str = datetime.datetime.now().isoformat()
	print("{}: Training SVM classifier".format(time_str))
	print("{}: size of training set is: {} images".format(time_str, len(training_data)))
	clf = LinearSVC()
	clf.fit(np.asarray(training_data), np.asarray(training_labels))
	joblib.dump(clf, 'linear_face_svm.pkl')
	time_str = datetime.datetime.now().isoformat()
	print("{}: Finished classifier".format(time_str))
	return


# Now run it
run_recognizer()
