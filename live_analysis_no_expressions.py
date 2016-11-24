import speech_recognition as sr
import text_class
import text_response
import emotions
import pandas as pd
import time
import matplotlib.pyplot as plt
import cozmo
import sys
# Warning Suppression
import warnings
warnings.filterwarnings("ignore")



def run(sdk_conn):
	'''The run method runs once Cozmo is connected.'''
	robot = sdk_conn.wait_for_robot()

	def process_audio(recognizer, audio):
		try:
			transcription = rec.recognize_google(audio)
		except sr.UnknownValueError:
			# API failed
			transcription = ""
		except sr.RequestError as e:
			# Request to API failed
			transcription = ""
		# print('Transcription', transcription)
		global bot_response
		bot_response = bot.respond_to(transcription)
		global cozmo_has_response
		cozmo_has_response = True
		# print('response: ', bot_response)
		sentiment_val = int(text_class.classify_text([transcription])[0])
		emot.add_speech_sentiment(sentiment[sentiment_val])

	bot = text_response.Chatbot()
	emot = emotions.EmotionCenter()
	emo_df = pd.DataFrame(emot.emotions, index=[0])
	rec = sr.Recognizer()
	sentiment = ["negative", "positive"]
	print(bot.get_started())
	bot_response = ''
	cozmo_has_response = False
	last_spoke = time.time()
	mic = sr.Microphone()
	with mic as source:
		rec.adjust_for_ambient_noise(mic)

	stop_listening = rec.listen_in_background(mic, process_audio)
	# Use start_time to get a set amount of time for the conversation (only a set amount will let me plot emotions)
	# start_time = time.time()
	current_emotion = emot.active_emotion
	while True:
		if emot.active_emotion != current_emotion:
			current_emotion = emot.active_emotion
			# if emot.active_emotion == 'neutral':
			# robot.play_anim_trigger(neutrality).wait_for_completed()
			# elif emot.active_emotion == 'happy':
			# robot.play_anim_trigger(happiness).wait_for_completed()
			# elif emot.active_emotion == 'sadness':
			# robot.play_anim_trigger(sadness).wait_for_completed()
			# elif emot.active_emotion == 'angry':
			# robot.play_anim_trigger(anger).wait_for_completed()
		if time.time() - last_spoke > 10:
			last_spoke = time.time()
			print('Cozmo is thinking...')
			stop_listening()
			if cozmo_has_response:
				print(bot_response)
				robot.say_text(bot_response).wait_for_completed()
				active_emotion = emot.active_emotion
				# if emot.active_emotion == 'neutral':
					# robot.play_anim_trigger(neutrality).wait_for_completed()
				# elif emot.active_emotion == 'happy':
					# robot.play_anim_trigger(happiness).wait_for_completed()
				# elif emot.active_emotion == 'sadness':
					# robot.play_anim_trigger(sadness).wait_for_completed()
				# elif emot.active_emotion == 'angry':
					# robot.play_anim_trigger(anger).wait_for_completed()
				cozmo_has_response = False
				stop_listening = rec.listen_in_background(mic, process_audio)

		emo_df = emo_df.append(emot.emotions, ignore_index=True)
		bot.user_feeling = emot.active_emotion

	styles = ['rs-', 'go-', 'b^-', 'ro-', 'y^-']
	plotter = emo_df.plot(title="Current Emotions", style=styles)
	plt.show()


if __name__ == '__main__':
	cozmo.setup_basic_logging()
	try:
		cozmo.connect(run)
	except cozmo.ConnectionError as e:
		sys.exit("A connection error occurred: %s" % e)
