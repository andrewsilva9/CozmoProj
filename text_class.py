import tensorflow as tf
import numpy as np
import data_util
from tensorflow.contrib import learn
import os
import csv

positive_data_file = "./data/rt-polaritydata/rt-polarity.pos"
negative_data_file = "./data/rt-polaritydata/rt-polarity.neg"
batch_size = 64
evaluate_on_train = False
checkpoint_dir = "./runs/1478835326/checkpoints"
allow_soft_placement = True
log_device_placement = False
config_prefs = tf.ConfigProto(allow_soft_placement=allow_soft_placement, log_device_placement=log_device_placement)
checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
graph = tf.Graph()

# print("Loading data...")
# if evaluate_on_train:
# 	x_unfiltered, y_test = data_util.load_data_and_labels(positive_data_file, negative_data_file)
# 	y_test = np.argmax(y_test, axis=1)
# else:
# 	x_unfiltered = ["a masterpiece four years in the making", "everything is off", "I am happy"]
# 	y_test = [1, 0, 1]

# vocab_path = os.path.join(checkpoint_dir, "..", "vocab")
# vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
# x_test = np.array(list(vocab_processor.transform(x_unfiltered)))


def classify_text(raw_input):
	# print("Transforming data...")
	vocab_path = os.path.join(checkpoint_dir, "..", "vocab")
	vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
	x_test = np.array(list(vocab_processor.transform(raw_input)))
	with graph.as_default():
		sess = tf.Session(config=config_prefs)
		with sess.as_default():
			# load graph
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
			saver.restore(sess, checkpoint_file)

			# get saved vars
			input_x = graph.get_operation_by_name("input_x").outputs[0]
			dropout_keep_probability = graph.get_operation_by_name("dropout_keep_probability").outputs[0]

			# tensors to classify
			predictions = graph.get_operation_by_name("output/predictions").outputs[0]

			# gen batches
			batch_data = data_util.batch_iter(x_test, batch_size, 1, shuffle=False)

			predicted_classes = []
			# Classify Batches
			for batch in batch_data:
				batch_pred = sess.run(predictions, {input_x: batch, dropout_keep_probability: 1.0})
				predicted_classes = np.concatenate([predicted_classes, batch_pred])
				# print(predicted_classes)
			# pred = sess.run(predicted_classes, {input_x: x_test, dropout_keep_probability:1.0})
			return predicted_classes


# print("Evaluating...")
# # checkpoint_file = tf.train.latest_checkpoint(checkpoint_dir)
# graph = tf.Graph()
# with graph.as_default():
# 	# Config preferences for session
# 	config_pref = tf.ConfigProto(allow_soft_placement = allow_soft_placement,
# 								 log_device_placement = log_device_placement)
# 	sess = tf.Session(config=config_pref)
# 	with sess.as_default():
# 		# Load saved graph
# 		saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
# 		saver.restore(sess, checkpoint_file)
#
# 		# Get saved variables by name
# 		input_x = graph.get_operation_by_name("input_x").outputs[0]
# 		dropout_keep_probability = graph.get_operation_by_name("dropout_keep_probability").outputs[0]
#
# 		# Tensors we want to classify
# 		predictions = graph.get_operation_by_name("output/predictions").outputs[0]
#
# 		# Generate batches
# 		batch_data = data_util.batch_iter(x_test, batch_size, 1, shuffle=False)
#
# 		predicted_classes = []
# 		# Classify batches
# 		for test_batch in batch_data:
# 			batch_predictions = sess.run(predictions, {input_x: test_batch, dropout_keep_probability: 1.0})
# 			predicted_classes = np.concatenate([predicted_classes, batch_predictions])
#
# # print accuracy if y_test exists
# if y_test is not None:
# 	correct = float(sum(predicted_classes == y_test))
# 	print("Number of test examples: ", len(y_test))
# 	print("Accuracy: ", correct/float(len(y_test)))
#
# printed_predictions = np.column_stack((np.array(x_unfiltered), predicted_classes))
# output_dir = os.path.join(checkpoint_dir, "..", "predictions.csv")
# print("Saving classes to: ", output_dir)
# with open(output_dir, 'w') as f:
# 	csv.writer(f).writerows(printed_predictions)
#
# for input_text, classification in zip(x_unfiltered, predicted_classes):
# 	print("Input: ", input_text)
# 	if classification:
# 		print("Class: Positive")
# 	else:
# 		print("Class: Negative")