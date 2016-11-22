import glob
import os
from shutil import copyfile

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"]  # Define emotion order
participants = glob.glob("../CozmoProj/source_emotion\\*")  # Returns a list of all folders with participant numbers
source_dir = os.listdir("../CozmoProj/source_emotion")
for dir in source_dir:
    if dir.startswith('.'):
        continue
    for session in os.listdir(os.path.join("../CozmoProj/source_emotion", dir)):
        for file in os.listdir(os.path.join("../CozmoProj/source_emotion", dir, session)):

            # Get coded emotion value
            emo_file = open(os.path.join("../CozmoProj/source_emotion", dir, session, file), 'r')
            emotion = int(float(emo_file.readline()))
            # Get path for emotion image
            source_file_emotion = os.listdir(os.path.join("../CozmoProj/source_images", dir, session))[-1]
            # Get path for neutral image
            source_file_neutral = os.listdir(os.path.join("../CozmoProj/source_images", dir, session))[0]
            # Generate destination path for neutral image
            destination_neutral = os.path.join("../CozmoProj/sorted_set/neutral", source_file_neutral)
            # Generate destination path for emotion image
            destination_emotion = os.path.join("../CozmoProj/sorted_set/", emotions[emotion], source_file_emotion)
            # Full emotion source path
            emotion_source = os.path.join("../CozmoProj/source_images", dir, session, source_file_emotion)
            # Full neutral source path
            neutral_source = os.path.join("../CozmoProj/source_images", dir, session, source_file_neutral)
            # Copy files over
            copyfile(emotion_source, destination_emotion)
            copyfile(neutral_source, destination_neutral)


# for x in participants:
#     part = "%s" % x[-4:]  # store current participant number
#     for sessions in glob.glob("%s\\*" % x):  # Store list of sessions for current participant
#         for files in glob.glob("%s\\*" % sessions):
#             current_session = files[20:-30]
#             file = open(files, 'r')
#
#             # emotions are encoded as a float, read line as float, then convert to integer.
#             emotion = int(float(file.readline()))
#             print(emotion)
#             # get path for last image in sequence, which contains the emotion
#             sourcefile_emotion = glob.glob("source_images\\%s\\%s\\*" % (part, current_session))[-1]
#
#             # do same for neutral image
#             sourcefile_neutral = glob.glob("source_images\\%s\\%s\\*" % (part, current_session))[0]
#
#             # Generate path to put neutral image
#             dest_neut = "sorted_set\\neutral\\%s" % sourcefile_neutral[25:]
#
#             # Do same for emotion containing image
#             dest_emot = "sorted_set\\%s\\%s" % (emotions[emotion], sourcefile_emotion[25:])
#
#             # copyfile(sourcefile_neutral, dest_neut)  # Copy file
#             # copyfile(sourcefile_emotion, dest_emot)  # Copy file
