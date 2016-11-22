import speech_recognition as sr
import text_class
import text_response
import webcam_recognizer as wcr
import emotions
import pandas as pd
import matplotlib.pyplot as plt

my_runner = wcr.CameraRunner()
bot = text_response.Chatbot()
emot = emotions.EmotionCenter()
emo_df = pd.DataFrame(emot.emotions, index=[0])
rec = sr.Recognizer()
sentiment = ["negative", "positive"]
print(bot.get_started())
my_runner.run(emot)

## I need to get expressions and transcription going in parallel
# DO like a while True: expression stuff constantly and have a variable and if it's true, go down the necessary bit of langauge processing
while True:
	print("I'm listening...")
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
	# emot.add_expression(expression)
	emot.add_speech_sentiment(sentiment[sentiment_val])
	emo_df = emo_df.append(emot.emotions, ignore_index=True)
	if transcription == 'quit':
		break
	print("Input: ", transcription)
	print("Sentiment: ", sentiment[sentiment_val])
	print("Response: ", response)
	print("Cozmo is feeling: ", emot.active_emotion)
	bot.user_feeling = emot.active_emotion
	print(emo_df.iloc[-1])
	# plotter = emo_df.plot(title="Current Emotions")
	# plt.pause(0.05)

