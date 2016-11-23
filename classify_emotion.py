# import os
import cv2
import numpy as np
from scipy import stats
from sklearn.externals import joblib
# Define class that can be instantiated and have images passed to it
# images will be processed, and an emotion will be returned


class EmotionClassifier:
    # For the Fisher face model (okay performance):
    def __init__(self):
        # Small Dataset Emotions:
        self.emotions = ["neutral", "anger", "happy", "sadness", "surprise"]  # Emotion list
        # self.emotions = ["anger", "disgust", "fear", "happy", "sad", "surprise", "neutral"]  # Emotion list

        self.models = []
        # for i in range(10):
        #     model_temp = cv2.face.createFisherFaceRecognizer()
        #     model_temp.load('fish_models/fish_model'
        #                     + str(i) + '.xml')
        #     self.models.append(model_temp)
        model_temp = cv2.face.createFisherFaceRecognizer()
        model_temp.load('new_model.xml')
        self.models = [model_temp]

    def classify_emotion(self, input_image):
        emotion_guesses = np.zeros((len(self.models), 1))
        for index in range(len(self.models)):
            prediction, confidence = self.models[index].predict(input_image)
            # emotion_guesses[index][1] = confidence
            # if self.emotions[prediction] == 'fear':
            #     prediction = 6  # sad
            #     # continue
            # elif self.emotions[prediction] == 'disgust':
            #     # continue
            #     prediction = 6  # sad
            # elif self.emotions[prediction] == 'contempt':
            #     # continue
            #     prediction = 1  # anger
            emotion_guesses[index][0] = prediction
        return int(stats.mode(emotion_guesses)[0][0])

    # For the SVM model (terrible performance):
    # def __init__(self):
    #     # Larger dataset emotions
    #     self.emotions = ["anger", "disgust", "fear", "happy", "sad", "surprise", "neutral"]  # Emotion list
    #     self.model = joblib.load('face_svm_small.pkl')
	#
	#
    # def classify_emotion(self, input_image):
    #     input_image = np.reshape(input_image, (1, 2304))
    #     return self.model.predict(input_image)
