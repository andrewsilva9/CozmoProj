import numpy as np
import re


def clean_string(string):
	"""
	Tokenization of strings.
	Taken from WildML, who took it from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
	:param string: string to clean
	:return: lowercase string, stripped of unwanted characters and contractions and cleaned
	"""
	string = re.sub(r"[^A-Za-z0-9(),!?\']", " ", string)
	string = re.sub(r"\'s", " \'s", string)
	string = re.sub(r"\'ve", " \'ve", string)
	string = re.sub(r"n\'t", " n\'t", string)
	string = re.sub(r"\'re", " \'re", string)
	string = re.sub(r"\'d", " \'d", string)
	string = re.sub(r"\'ll", " \'ll", string)
	string = re.sub(r",", " , ", string)
	string = re.sub(r"!", " ! ", string)
	string = re.sub(r"\(", " \( ", string)
	string = re.sub(r"\)", " \) ", string)
	string = re.sub(r"\?", " \? ", string)
	string = re.sub(r"\s{2,}", " ", string)
	return string.strip().lower()


def load_data_and_labels(pos_file, neg_file):
	# Load in data and split strings
	positive_data = list(open(pos_file, "r").readlines())
	negative_data = list(open(neg_file, "r").readlines())
	positive_data = [s.strip() for s in positive_data]
	negative_data = [s.strip() for s in negative_data]
	x_text = positive_data + negative_data
	x_text = [clean_string(text) for text in x_text]
	# Label generation:
	positive_labels = [[0, 1] for _ in positive_data]
	negative_labels = [[1, 0] for _ in negative_data]
	y = np.concatenate([positive_labels, negative_labels], 0)
	return [x_text, y]


def batch_iter(data, batch_size, num_epochs, shuffle=True):
	data = np.array(data)
	data_size = len(data)
	num_batches_per_epoch = int(data_size/batch_size) + 1
	for epoch in range(num_epochs):
		if shuffle:
			shuffled_indices = np.random.permutation(np.arange(data_size))
			data = data[shuffled_indices]
		for batch in range(num_batches_per_epoch):
			start_index = batch * batch_size
			end_index = min(start_index + batch_size, data_size)
			yield data[start_index:end_index]
