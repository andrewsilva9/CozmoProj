class EmotionCenter:
	def __init__(self):
		self.emotion_decay_rate = 0.95
		self.emotion_spike_factor = 5
		self.emotions = {'happy': 0.0, 'sadness': 0.0, 'neutral': 1.0, 'anger': 0.0}
		self.active_emotion = 'neutral'
		self.last_emotions = []

	def add_expression(self, input_string):
		if input_string is 'neutral':
			self.emotions['neutral'] += 0.2
			self.reevaluate()
			return
		if input_string in self.emotions:
			if input_string in self.last_emotions:
				self.emotions[input_string] += 0.5
			self.last_emotions.append(input_string)
			self.last_emotions = self.last_emotions[-5:]
		self.reevaluate()

	def get_current_emotion(self):
		return self.active_emotion

	def add_speech_sentiment(self, input_string):
		if input_string == 'positive':
			self.emotions['happy'] += 0.3
			self.emotions['sadness'] -= 0.2
			self.emotions['anger'] -= 0.2
		else:
			self.emotions['sadness'] += 0.2
			self.emotions['anger'] += 0.2
			self.emotions['happy'] -= 0.2
		self.reevaluate()

	def reevaluate(self):

		self.emotions[self.active_emotion] *= self.emotion_decay_rate
		# If happy / sad or angry are close, go to neutral
		if abs(self.emotions['happy'] - self.emotions['sadness']) < 0.5 or abs(self.emotions['happy'] - self.emotions['anger']) < 0.5:
			new_max = 'neutral'
		else:
			new_max = max(self.emotions, key=lambda v: self.emotions[v])
		if self.active_emotion != new_max:
			self.emotions[new_max] += self.emotion_spike_factor
			self.active_emotion = new_max
