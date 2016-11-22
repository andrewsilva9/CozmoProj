import cv2
import os

face_finder = cv2.CascadeClassifier("/Users/andrewsilva/opencv-3.1.0/data/haarcascades/haarcascade"
										 "_frontalface_default.xml")
face_finder2 = cv2.CascadeClassifier("/Users/andrewsilva/opencv-3.1.0/data/haarcascades/haarcascade"
										  "_frontalface_alt2.xml")
face_finder3 = cv2.CascadeClassifier("/Users/andrewsilva/opencv-3.1.0/data/haarcascades/haarcascade"
										  "_frontalface_alt.xml")
face_finder4 = cv2.CascadeClassifier("/Users/andrewsilva/opencv-3.1.0/data/haarcascades/haarcascade"
										  "_frontalface_alt_tree.xml")
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Define emotions


def detect_faces(emotion):
	# Get list of images with emotion
	files = os.listdir(os.path.join("../CozmoProj/sorted_set", emotion))

	filenumber = 0
	for f in files:
		if f.startswith('.'):
			continue
		f = os.path.join("../CozmoProj/sorted_set", emotion, f)
		frame = cv2.imread(f)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		face1 = face_finder.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
												  flags=cv2.CASCADE_SCALE_IMAGE)
		face2 = face_finder2.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
												   flags=cv2.CASCADE_SCALE_IMAGE)
		face3 = face_finder3.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
												   flags=cv2.CASCADE_SCALE_IMAGE)
		face4 = face_finder4.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5),
												   flags=cv2.CASCADE_SCALE_IMAGE)

		if len(face1) == 1:
			face = face1[0]
		elif len(face2) == 1:
			face = face2[0]
		elif len(face3) == 1:
			face = face3[0]
		elif len(face4) == 1:
			face = face4[0]
		else:
			continue
		# Cut and save face
		# scale image
		gray = gray[face[1]:face[1] + face[3], face[0]:face[0] + face[2]]

		try:
			out = cv2.resize(gray, (350, 350))  # Resize face so all images have same size
			outpath = os.path.join("../CozmoProj/dataset", emotion, str(filenumber)+".jpg")
			cv2.imwrite(outpath, out)  # Write image
		except:
			pass  # If error, pass file
		filenumber += 1  # Increment image number


def flip_faces(emotion):
	files = os.listdir(os.path.join("../CozmoProj/dataset", emotion))
	filenumber = 0
	for f in files:
		if f.startswith('.'):
			continue
		f = os.path.join("../CozmoProj/dataset", emotion, f)
		frame = cv2.imread(f, 0)
		outimg = cv2.flip(frame, flipCode=1)
		outpath = os.path.join("../CozmoProj/dataset", emotion, str(filenumber)+"f.jpg")
		cv2.imwrite(outpath, outimg)
		filenumber += 1


# for emotion in emotions:
# 	detect_faces(emotion)  # Call function
# 	# flip_faces(emotion)
flip_faces('happy')
flip_faces('sadness')
