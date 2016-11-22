import tensorflow as tf
import numpy as np
import os
import time
import datetime
import data_util
from text_convnet import TextConvNet
from tensorflow.contrib import learn

# Data Params
validation_percent = 0.1
positive_datafile = './data/rt-polaritydata/rt-polarity.pos'
negative_datafile = './data/rt-polaritydata/rt-polarity.neg'

# Model Params
embedding_dimension = 128
filter_sizes = [3, 4, 5]
num_filters = 128
dropout_keep_probability = 0.5
l2_reg_lambda = 0.0

# Training Params
batch_size = 64
num_epochs = 200
evaluate_every = 100
checkpoint_every = 100

# Platform Params
soft_placement = True
log_devices = False

x_text, y = data_util.load_data_and_labels(positive_datafile, negative_datafile)
max_doc_length = max(len(x.split(" ")) for x in x_text)
vocab_processor = learn.preprocessing.VocabularyProcessor(max_doc_length)
x = np.array(list(vocab_processor.fit_transform(x_text)))

# Shuffle Data
np.random.seed(10)
shuffled_indices = np.random.permutation(np.arange(len(y)))
x = x[shuffled_indices]
y = y[shuffled_indices]

# Train / Test Split
test_end_index = -1 * int(validation_percent * len(y))
x_train, x_test = x[:test_end_index], x[test_end_index:]
y_train, y_test = y[:test_end_index], y[test_end_index:]

# Training:
with tf.Graph().as_default():
	session_config = tf.ConfigProto(allow_soft_placement=soft_placement, log_device_placement=log_devices)
	sess = tf.Session(config=session_config)
	with sess.as_default():
		cnn = TextConvNet(
			sequence_length=x_train.shape[1],
			num_classes=y_train.shape[1],
		 	vocab_size=len(vocab_processor.vocabulary_),
			embedding_size=embedding_dimension,
		    filter_sizes=filter_sizes,
		    num_filters=num_filters,
		    l2_reg_lambda=l2_reg_lambda)
		global_step = tf.Variable(0, name="global_step", trainable=False)
		optimizer = tf.train.AdamOptimizer()
		grads_and_vars = optimizer.compute_gradients(cnn.loss)
		train_op = optimizer.apply_gradients(grads_and_vars, global_step=global_step)

		# Keep track of gradient values and sparsity
		grad_summaries = []
		for g, v in grads_and_vars:
			if g is not None:
				grad_hist_summary = tf.histogram_summary("{}/grad/hist".format(v.name), g)
				sparse_summary = tf.scalar_summary("{}/grad/sparsity".format(v.name), tf.nn.zero_fraction(g))
				grad_summaries.append(grad_hist_summary)
				grad_summaries.append(sparse_summary)
		grad_summaries_merged = tf.merge_summary(grad_summaries)

	# Output directory for model and summaries
	timestamp = str(int(time.time()))
	out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
	print("Writing to {}\n".format(out_dir))

	loss_summary = tf.scalar_summary("loss", cnn.loss)
	accuracy_summary = tf.scalar_summary("accuracy", cnn.accuracy)
	train_summary_op = tf.merge_summary([loss_summary, accuracy_summary, grad_summaries_merged])
	train_summary_dir = os.path.join(out_dir, "summaries", "train")
	train_summary_writer = tf.train.SummaryWriter(train_summary_dir, sess.graph)

	val_summary_op = tf.merge_summary([loss_summary, accuracy_summary])
	val_summary_dir = os.path.join(out_dir, "summaries", "val")
	val_summary_writer = tf.train.SummaryWriter(val_summary_dir, sess.graph)

	# Checkpoints
	checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
	checkpoint_prefix = os.path.join(checkpoint_dir, "model")
	if not os.path.exists(checkpoint_dir):
		os.makedirs(checkpoint_dir)
	saver = tf.train.Saver(tf.all_variables())

	# Save Vocab
	vocab_processor.save(os.path.join(out_dir, "vocab"))

	# Init all variables
	sess.run(tf.initialize_all_variables())

	def train_step(x_batch, y_batch):
		# Run one training step
		feed_dict = {
			cnn.input_x: x_batch,
			cnn.input_y: y_batch,
			cnn.dropout_keep_probability: dropout_keep_probability
		}
		_, step, summaries, loss, accuracy = sess.run([train_op, global_step, train_summary_op, cnn.loss, cnn.accuracy],
													feed_dict=feed_dict)
		time_str = datetime.datetime.now().isoformat()
		print("{}: step {}, loss {:g}, accuracy {:g}".format(time_str, step, loss, accuracy))
		train_summary_writer.add_summary(summaries, step)

	def dev_step(x_batch, y_batch, writer=None):
		# Evaluate model on test set
		feed_dict = {
			cnn.input_x: x_batch,
			cnn.input_y: y_batch,
			cnn.dropout_keep_probability: 1.0
		}
		step, summaries, loss, accuracy = sess.run([global_step, val_summary_op, cnn.loss, cnn.accuracy],
													feed_dict=feed_dict)
		time_str = datetime.datetime.now().isoformat()
		print("{}: step {}, loss{:g}, accuracy{:g}".format(time_str, step, loss, accuracy))
		if writer:
			writer.add_summary(summaries, step)

	# Generate batches
	batches = data_util.batch_iter(list(zip(x_train, y_train)), batch_size=batch_size, num_epochs=num_epochs)
	# Training loop
	for batch in batches:
		x_batch, y_batch = zip(*batch)
		train_step(x_batch, y_batch)
		current_step = tf.train.global_step(sess, global_step)
		if current_step % evaluate_every == 0:
			print("\n Evaluation: ")
			dev_step(x_test, y_test, writer=val_summary_writer)
			print("")
		if current_step % checkpoint_every == 0:
			path = saver.save(sess, checkpoint_prefix, global_step=current_step)
			print("Saved checkpoint of model to {} \n".format(path))
