import speech_recognition as sr
import text_class
import text_response
import webcam_recognizer as wcr
import emotions
import pandas as pd
import time
import matplotlib.pyplot as plt

my_runner = wcr.CameraRunner()
bot = text_response.Chatbot()
emot = emotions.EmotionCenter()
emo_df = pd.DataFrame(emot.emotions, index=[0])
rec = sr.Recognizer()
sentiment = ["negative", "positive"]
print(bot.get_started())
bot_response = ''
last_spoke = time.time()

while time.time() - last_spoke < 45:
	print("I'm listening...")
	expression = my_runner.run()
	emot.add_expression(expression)
	with sr.Microphone() as source:
		audio = rec.listen(source=source)

	try:
		transcription = rec.recognize_google(audio)
	except sr.UnknownValueError:
		# API failed
		transcription = ""
	except sr.RequestError as e:
		# Request to API failed
		transcription = ""
	# expression = my_runner.run()

	# transcription = input("> ")
	response = bot.respond_to(transcription)
	sentiment_val = int(text_class.classify_text([transcription])[0])
	emot.add_speech_sentiment(sentiment[sentiment_val])
	emo_df = emo_df.append(emot.emotions, ignore_index=True)
	if transcription == 'quit':
		break
	print("Input: ", transcription)
	print("Sentiment: ", sentiment[sentiment_val])
	print("Response: ", response)
	print("Cozmo is feeling: ", emot.active_emotion)
	bot.user_feeling = emot.active_emotion
# print(emo_df.iloc[-1])
plotter = emo_df.plot(title="Current Emotions")
plt.show()

# mic = sr.Microphone()
# with mic as source:
# 	rec.adjust_for_ambient_noise(mic)
#
# def transcribe_sentiment_respond(recognizer, audio):
# 	try:
# 		transcription = rec.recognize_google(audio)
# 	except sr.UnknownValueError:
# 		# API failed
# 		transcription = ""
# 	except sr.RequestError as e:
# 		# Request to API failed
# 		transcription = ""
# 	print(transcription)
# 	bot_response = bot.respond_to(transcription)
# 	sentiment_val = int(text_class.classify_text([transcription])[0])
# 	emot.add_speech_sentiment(sentiment[sentiment_val])
#
# have_speech = False
# process_language = rec.listen_in_background(mic, transcribe_sentiment_respond)
# starter = time.time()
# while True:
# 	# Get faces every loop
# 	expression = my_runner.run()
# 	emot.add_expression(expression)
# 	# Say we have speech every 5 seconds
# 	if time.time() - last_spoke > 5:
# 		last_spoke = time.time()
# 		print("Have speech!")
# 		have_speech = True
# 	# If we have speech, process it and say we don't have anymore for next few loops
# 	if have_speech:
# 		process_language()
# 		print(bot_response)
# 		have_speech = False
# 	emo_df.append(emot.emotions, ignore_index=True)
