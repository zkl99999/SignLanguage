import numpy as np
from keras.datasets import mnist # subroutines for fetching the MNIST dataset
from keras.models import Model # basic class for specifying and training a neural network
from keras.layers import Input, Dense # the two types of neural network layer we will be using
from keras.utils import np_utils # utilities for one-hot encoding of ground truth values
from keras.models import load_model
import random
import confusion_matrix
# para
task_is_train = True

test_len = 1000
num_classes = 6

batch_size = 128 # in each iteration, we consider 128 training examples at once
num_epochs = 20 # we iterate twenty times over the entire training set
hidden_size = 512 # there will be 512 neurons in both hidden layers
saved_model_name = "lx_zy.h5"
finger_data_dim = 63



# read data file and slice train and test set
data = np.loadtxt("../data/data.txt", delimiter = ",")
x = data[:, :-1]
x_abs_max = max(x.max(), -x.min()) + 1 #TODO
x /= x_abs_max

print "x_abs_max is " + str(x_abs_max)

train_len = len(data) - test_len
test_set = np.empty((test_len, finger_data_dim + 1))
train_set = np.empty((train_len, finger_data_dim + 1))

p = test_len * 1.0 / len(data)

test_size = 0
train_size = 0

for v in data:
	if (test_size < test_len) and (random.random() <= p):
		test_set[test_size] = v
		test_size = test_size + 1
	else:
		if(train_size < train_len):
			train_set[train_size] = v
			train_size = train_size + 1
		else:
			test_set[test_size] = v
			test_size = test_size + 1

test_x = test_set[:, :-1]
test_y = test_set[:, -1:].reshape(-1, ).astype("int32")
test_y = np_utils.to_categorical(test_y, num_classes) # One-hot encode the labels


train_x = train_set[:, :-1]
train_y = train_set[:, -1:].reshape(-1, ).astype("int32")
train_y = np_utils.to_categorical(train_y, num_classes) # One-hot encode the labels


# print train_x
# print train_y
# print "=" * 10	
# print test_x
# print test_y
print "train_x.shape: " + str(train_x.shape)
print "train_y.shape: " + str(train_y.shape)
print "=" * 20	
print "test_x.shape: " + str(test_x.shape)
print "test_y.shape: " + str(test_y.shape)

if task_is_train:
	inp = Input(shape=(finger_data_dim,)) # Our input is a 1D vector of size 63
	hidden_1 = Dense(hidden_size, activation='relu')(inp) # First hidden ReLU layer
	hidden_2 = Dense(hidden_size, activation='relu')(hidden_1) # Second hidden ReLU layer
	out = Dense(num_classes, activation='softmax')(hidden_2) # Output softmax layer

	model = Model(input=inp, output=out) # To define a model, just specify its input and output layers

	model.compile(loss='categorical_crossentropy', # using the cross-entropy loss function
	              optimizer='adam', # using the Adam optimiser
	              metrics=['accuracy']) # reporting the accuracy

	model.fit(train_x, train_y, # Train the model using the training set...
	          batch_size=batch_size, nb_epoch=num_epochs,
	          verbose=1, validation_split=0.08) # ...holding out 10% of the data for validation
	print "\n"
else:
	model = load_model(saved_model_name)

print model.evaluate(test_x, test_y, verbose=1) # Evaluate the trained model on the test set!
confusion_matrix.get_confusion_matrix(model, test_x, test_y)
model.save(saved_model_name)
