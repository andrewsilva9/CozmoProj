import speech_recognition as sr
import text_class
import text_response
import emotions
import pandas as pd
import time
import matplotlib.pyplot as plt
import cozmo
import sys
from random import randint
# Warning Suppression
import warnings
warnings.filterwarnings("ignore")

bot = text_response.Chatbot()
emot = emotions.EmotionCenter()
emo_df = pd.DataFrame(emot.emotions, index=[0])
rec = sr.Recognizer()
sentiment = ["negative", "positive"]
print(bot.get_started())
bot_response = ''
cozmo_has_response = False
last_spoke = time.time()
start_time = time.time()
mic = sr.Microphone()
with mic as source:
	rec.adjust_for_ambient_noise(mic)


def process_audio(recognizer, audio):
	print('Cozmo is thinking...')
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


def run(sdk_conn):
	# Lists of animations to randomly pull from
	angry_anims = [cozmo.anim._AnimTrigger(name='DriveStartAngry', id=39),
	               cozmo.anim._AnimTrigger(name='DriveEndAngry', id=33),
	               cozmo.anim._AnimTrigger(name='DriveLoopAngry', id=36),
	               cozmo.anim._AnimTrigger(name='FrustratedByFailure', id=57),
	               cozmo.anim._AnimTrigger(name='FrustratedByFailureMajor', id=58),
	               cozmo.anim._AnimTrigger(name='KnockOverFailure', id=82),
	               cozmo.anim._AnimTrigger(name='MajorFail', id=89),
	               cozmo.anim._AnimTrigger(name='PounceFail', id=162),
	               cozmo.anim._AnimTrigger(name='RequestGameDrivingFail', id=183),
	               cozmo.anim._AnimTrigger(name='RequestGamePickupFail', id=208),
	               cozmo.anim._AnimTrigger(name='CubePounceLoseSession', id=23),
	               cozmo.anim._AnimTrigger(name='RequestGameDrivingFail', id=183),
	               cozmo.anim._AnimTrigger(name='CubePounceLoseRound', id=22),
	               cozmo.anim._AnimTrigger(name='CantHandleTallStack', id=8)
	               ]
	sad_anims = [cozmo.anim._AnimTrigger(name='RequestGameKeepAwayDeny0', id=186),
	             cozmo.anim._AnimTrigger(name='RequestGameKeepAwayDeny1', id=187),
	             cozmo.anim._AnimTrigger(name='CubeMovedUpset', id=13)
	             ]
	happy_anims = [cozmo.anim._AnimTrigger(name='BuildPyramidSuccess', id=7),
	               cozmo.anim._AnimTrigger(name='CubePounceFake', id=14),
	               cozmo.anim._AnimTrigger(name='CubePounceWinHand', id=26),
	               cozmo.anim._AnimTrigger(name='CubePounceWinRound', id=27),
	               cozmo.anim._AnimTrigger(name='CubePounceWinSession', id=28),
	               cozmo.anim._AnimTrigger(name='KnockOverSuccess', id=86),
	               cozmo.anim._AnimTrigger(name='MajorWin', id=90),
	               cozmo.anim._AnimTrigger(name='OnLearnedPlayerName', id=106),
	               cozmo.anim._AnimTrigger(name='OnSpeedtapGameCozmoWinLowIntensity', id=120),
	               cozmo.anim._AnimTrigger(name='OnSpeedtapGameCozmoWinHighIntensity', id=119),
	               cozmo.anim._AnimTrigger(name='OnSpeedtapRoundCozmoWinHighIntensity', id=127),
	               cozmo.anim._AnimTrigger(name='OnSpeedtapRoundCozmoWinLowIntensity', id=128),
	               cozmo.anim._AnimTrigger(name='PounceSuccess', id=166),
	               cozmo.anim._AnimTrigger(name='RollBlockSuccess', id=227)
	               ]
	neutral_anims = [cozmo.anim._AnimTrigger(name='NeutralFace', id=101),
	                 cozmo.anim._AnimTrigger(name='NothingToDoBoredIdle', id=103),
	                 cozmo.anim._AnimTrigger(name='OnboardingIdle', id=143)
	                 ]


	'''The run method runs once Cozmo is connected.'''
	robot = sdk_conn.wait_for_robot()


	global last_spoke
	global cozmo_has_response
	global bot_response
	global emo_df
	stop_listening = rec.listen_in_background(mic, process_audio)
	# Use start_time to get a set amount of time for the conversation (only a set amount will let me plot emotions)
	# start_time = time.time()
	current_emotion = emot.active_emotion
	while time.time() - start_time < 120:
		if emot.active_emotion != current_emotion:
			current_emotion = emot.active_emotion
			if emot.active_emotion == 'neutral':
				robot.play_anim_trigger(neutral_anims[randint(0, len(neutral_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'happy':
				robot.play_anim_trigger(happy_anims[randint(0, len(happy_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'sadness':
				robot.play_anim_trigger(sad_anims[randint(0, len(sad_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'angry':
				robot.play_anim_trigger(angry_anims[randint(0, len(angry_anims)-1)],
				                        loop_count=1).wait_for_completed()
		if time.time() - last_spoke > 15:
			last_spoke = time.time()
			stop_listening()
			print(bot_response)
			# robot.say_text(bot_response).wait_for_completed()
			if emot.active_emotion == 'neutral':
				robot.play_anim_trigger(neutral_anims[randint(0, len(neutral_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'happy':
				robot.play_anim_trigger(happy_anims[randint(0, len(happy_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'sadness':
				robot.play_anim_trigger(sad_anims[randint(0, len(sad_anims)-1)],
				                        loop_count=1).wait_for_completed()
			elif emot.active_emotion == 'angry':
				robot.play_anim_trigger(angry_anims[randint(0, len(angry_anims)-1)],
				                        loop_count=1).wait_for_completed()
			stop_listening = rec.listen_in_background(mic, process_audio)

		emo_df = emo_df.append(emot.emotions, ignore_index=True)
		bot.user_feeling = emot.active_emotion

	styles = ['rs-', 'go-', 'b^-', 'ro-', 'y^-']
	plotter = emo_df.plot(title="Current Emotions", style=styles)
	plt.show()


cozmo.setup_basic_logging()
cozmo.connect(run)
