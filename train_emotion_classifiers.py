import cv2
import os
import datetime
import numpy as np
import random

# emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Emotion list
emotions = ["neutral", "anger", "happy", "sadness", "surprise"]  # Emotion list

# emotions = ["anger", "happy", "sadness", "surprise", "neutral"]  # Emotion list
fishface = cv2.face.createFisherFaceRecognizer()  # Initialize fisher face classifier

data = {}


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
	training = files[:int(len(files) * 1)]  # get first 80% of file list
	prediction = files[-int(len(files) * 0):]  # get last 20% of file list
	return training, prediction


def make_sets():
	training_data = []
	training_labels = []
	prediction_data = []
	prediction_labels = []
	for emotion in emotions:
		training, prediction = get_files(emotion)
		source_path = os.path.join("../CozmoProj/dataset", emotion)
		# Append data to training and prediction list, and generate labels 0-7
		for item in training:
			if item.startswith('.'):
				continue
			gray = cv2.imread(os.path.join(source_path, item), 0)  # open image
			# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert to grayscale
			training_data.append(gray)  # append image array to training data list
			training_labels.append(emotions.index(emotion))

		for item in prediction:  # repeat above process for prediction set
			if item.startswith('.'):
				continue
			gray = cv2.imread(os.path.join(source_path, item), 0)
			# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			prediction_data.append(gray)
			prediction_labels.append(emotions.index(emotion))

	return training_data, training_labels, prediction_data, prediction_labels


def run_recognizer(num_run=0):
	training_data, training_labels, prediction_data, prediction_labels = make_sets()
	time_str = datetime.datetime.now().isoformat()
	print("{}: Training Fisher face classifier".format(time_str))
	print("{}: size of training set is: {} images".format(time_str, len(training_data)))
	fishface.train(training_data, np.asarray(training_labels))
	# fishface.save('fish_models/fish_model' + str(num_run) + '.xml')
	fishface.save('new_model2.xml')
	time_str = datetime.datetime.now().isoformat()
	print("{}: Predicting test set".format(time_str))
	cnt = 0
	correct = 1
	incorrect = 0
	for image in prediction_data:
		pred, conf = fishface.predict(image)
		if pred == prediction_labels[cnt]:
			correct += 1
			cnt += 1
		else:
			incorrect += 1
			cnt += 1
	return (100 * correct) / (correct + incorrect)


# Now run it
correct = run_recognizer()
time_str = datetime.datetime.now().isoformat()
print("{}: {:.4f} percent correct".format(time_str, correct))
# metascore = []
# for i in range(0, 10):
# 	correct = run_recognizer(num_run=i)
# 	time_str = datetime.datetime.now().isoformat()
# 	print("{}: Run {}: {:.4f} percent correct".format(time_str, i, correct))
# 	metascore.append(correct)
# time_str = datetime.datetime.now().isoformat()
# print("{}: Final score: {:.4f} percent correct".format(time_str, np.mean(metascore)))
