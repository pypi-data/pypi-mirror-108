import numpy as np

import mnist
import sidSimpleNN.myNN as myNN 
# import myNN as myNN 
# import myNN 

def run():

	# load data
	num_classes = 10
	train_images = mnist.train_images() #[60000, 28, 28]
	train_labels = mnist.train_labels()
	test_images = mnist.test_images()
	test_labels = mnist.test_labels()

	# print("Training...")

	# # data processing
	X_train = train_images.reshape(train_images.shape[0], train_images.shape[1]*train_images.shape[2]).astype('float32') #flatten 28x28 to 784x1 vectors, [60000, 784]
	x_train = X_train / 255 #normalization
	y_train = np.eye(num_classes)[train_labels] #convert label to one-hot

	X_test = test_images.reshape(test_images.shape[0], test_images.shape[1]*test_images.shape[2]).astype('float32') #flatten 28x28 to 784x1 vectors, [60000, 784]
	x_test = X_test / 255 #normalization
	y_test = test_labels

	np.random.seed(1)

	net = myNN.Network(
                 num_nodes_in_layers = [784, 20, 10], 
                 batch = 1,
                 epochs = 6,
                 learning_rate = 0.001, 
                 weights_file=None,
                 chosenActivation='tanh',
                 chosenLoss='MSE',
                 # name='tempnet3'
                 # weightsAndBias_file = 'digitRecog',
                 # includeWeightsBias=True

             )

	print('before training , testing with test dataset')
	# net.chosenLoss='CE'
	# net.applySoftmax=True
	# net.applyRegularization=False
	# net.regularizationConst=0.01
	# net.calcLoss=False
	# net.saveWeightsBiasJSON()
	message=net.test(x_test, y_test)


	net.train(x_train, y_train)
	net.save()
	net.lossGraph()
	print('before training , testing with test dataset')
	print(message)

	print("after training")
	net.test(x_test, y_test)
	net.showModel()

	# net.applyRegularization
	# net.regularizationConst=0.0001
	# net.applySoftmax=False
	# np.set_printoptions(suppress=True)
	# net.feedforward(x_train[0])
	# z=net.fasqwdfzeop
	#activation applied
	# a=net.rasqwdfzeopop
	# print(z)
	# print(a)
	# import function
	
	# print(function.tanh([[-26.33910613 ,  7.56055857, -47.45400574,   1.65570075,  -5.44114857,
	#  -23.85436946,  11.8361229,   16.61606579, -43.88570782, -27.62500334]]))

	# print(np.array(list(map(np.tanh,z))))

if __name__=='__main__':
	run()


