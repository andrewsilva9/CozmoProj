import random
import datetime


class Chatbot:
	def __init__(self):
		# Things Cozmo should know
		self.introduced = False
		self.user_name = None
		current_hour = datetime.datetime.now().hour
		if current_hour < 12:
			self.day_part = 'morning'
		elif current_hour < 17:
			self.day_part = 'afternoon'
		else:
			self.day_part = 'evening'
		self.last_topic = None
		self.current_subject = None
		self.user_feeling = None
		self.last_phrase = None
		# Library of lines:
		# last_topic = name
		self.name_question = "What's your name?"
		# last_topic = greeting
		self.greetings = ['Hello!', 'Hi there!', 'Hey!']
		# last_topic = starter
		self.starter_questions = ['How are you?', 'How is your {} going?'.format(self.day_part)]
		# last_topic = feeling
		self.feeling_questions = ['How are you feeling?']
		# last_topic = morning
		self.morning_questions = ['How does your day look today?', 'What are you doing today?',
								  'What are you doing later?', 'How has your morning been so far?']
		# last_topic = afternoon
		self.afternoon_questions = ['How has your day been so far?', 'Are you doing anything fun later?',
									'How was your morning?']
		# last_topic = evening
		self.evening_questions = ['How was your day?', 'What was the best part of your day?', 'How is your evening so far?']
		# last_topic = tellmore
		self.tell_me_more = ['Tell me more about ',
							 'I want to hear more about ']
		# last_topic = why
		self.why = ['Why is that?', 'Why do you think that is?', 'Could you explain that?']
		# last_topic = unknown
		self.unknown = ['Could you repeat that?', "Sorry, I didn't get that", "Sorry, I couldn't understand that"]
		# last_topic = me
		self.about_me = 'My name is Cozmo! I am a Cozmo.'
		self.ramble_questions = ['Are you excited for the holidays?', "What's your favorite food?",
								 "What's your favorite sports team?", "What do you do most days?",
								 "What do you want to talk about?"]

	def get_started(self):
		greeting = self.greetings[random.randint(0, len(self.greetings)-1)]
		greeting += '\n'
		greeting += self.about_me
		self.last_topic = 'greeting'
		self.last_phrase = greeting
		return greeting

	def respond_to(self, input_text):
		words = input_text.split()
		# no input or failed mic reading
		if len(words) == 0:
			self.last_topic = 'unknown'
			return self.unknown[random.randint(0, len(self.unknown) - 1)]
		# Not finished with introductions, follow that path
		# (we're assuming that elsewhere someone will call on self.greetings)
		if self.introduced is False:
			# if we don't have their name, get it
			if self.last_topic == 'greeting' or self.last_topic == 'unknown' and self.user_name is None:
				# if they said : hi my name is andrew, get andrew out and move on
				if 'name' in words:
					self.user_name = words[words.index('name') + 2]
					self.last_topic = 'starter'
					phrase = 'Hi {}! \n'.format(self.user_name)
					self.introduced = True
					phrase += self.starter_questions[random.randint(0, len(self.starter_questions)-1)]
					self.last_phrase = phrase
					return phrase
				# if they didn't say their name, ask
				self.last_topic = 'name'
				return self.name_question
			# we have a name, move out of introductions
			if self.last_topic == 'name':
				self.introduced = True
				if 'name' in words:
					self.user_name = words[words.index('name') + 2]
					phrase = 'Hi {}! \n'.format(self.user_name)
				else:
					self.user_name = words[0]
					phrase = 'Hi {}! \n'.format(self.user_name)
				self.last_topic = 'starter'
				self.introduced = True
				phrase += self.starter_questions[random.randint(0, len(self.starter_questions)-1)]
				self.last_phrase = phrase
				return phrase
		# Out of introductions
		if self.last_topic == 'starter':
			phrase = ''
			# If they say "good how are you?" for example
			if 'you' in words or 'you?' in words:
				if self.user_feeling is not None:
					phrase += "I'm feeling {} today \n".format(self.user_feeling)
			phrase += self.day_part_response()
			return phrase
		elif self.last_topic == 'morning' or self.last_topic == 'afternoon' or self.last_topic == 'evening' or self.last_topic == 'ramble':
			phrase = self.tell_me_more[random.randint(0, len(self.tell_me_more)-1)]
			phrase += self.current_subject
			self.last_topic = 'tellmore'
			self.last_phrase = phrase
			return phrase
		elif self.last_topic == 'tellmore':
			phrase = self.day_part_response()
			# self.last_topic handled by the day part response
			return phrase
		elif self.last_topic == 'unknown':
			phrase = 'Oh okay, thanks for repeating that \n'
			phrase += self.last_phrase
			self.last_phrase = phrase
			self.last_topic = 'starter'
			return phrase
		elif self.last_topic == 'GARETH':
			return 'Cozmo is fast asleep...'

	def day_part_response(self):
		# Ask about morning
		phrase = ''
		if self.day_part == 'morning' and len(self.morning_questions) > 0:
			self.last_topic = 'morning'
			next_bit = self.morning_questions[random.randint(0, len(self.morning_questions) - 1)]
			self.morning_questions.remove(next_bit)
			self.current_subject = 'your morning'
			phrase += next_bit
		# Ask about afternoon
		elif self.day_part == 'afternoon' and len(self.afternoon_questions) > 0:
			self.last_topic = 'afternoon'
			next_bit = self.afternoon_questions[random.randint(0, len(self.afternoon_questions) - 1)]
			self.afternoon_questions.remove(next_bit)
			if 'day' in next_bit:
				self.current_subject = 'your day'
			elif 'morning?' in next_bit:
				self.current_subject = 'your morning'
			else:
				self.current_subject = 'your afternoon'
			phrase += next_bit
		# Ask about evening
		elif self.day_part == 'evening' and len(self.evening_questions) > 0:
			self.last_topic = 'evening'
			part_deux = self.evening_questions[random.randint(0, len(self.evening_questions) - 1)]
			self.evening_questions.remove(part_deux)
			if 'day' in part_deux or 'day?' in part_deux:
				self.current_subject = 'your day'
			else:
				self.current_subject = 'your evening'
			phrase += part_deux
		if phrase == '' and len(self.ramble_questions) > 0:
			phrase = self.ramble_questions[random.randint(0, len(self.ramble_questions)-1)]
			self.ramble_questions.remove(phrase)
			self.current_subject = 'that'
			self.last_topic = 'ramble'
		elif phrase == '':
			phrase = "I'm feeling a bit tired. Thanks for the chat, I'll talk to you later!"
			self.current_subject = 'goodbye'
			self.last_topic = 'GARETH'
			print(self.last_topic)
		self.last_phrase = phrase
		return phrase
