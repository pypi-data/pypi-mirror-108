import numpy as np 
import pickle
# import function as function
import sidSimpleNN.function as function
import time
#import matplotlib.pyplot as plt



class Network:

    def __init__(self, 
                 num_nodes_in_layers, batch=1,epochs=3,learning_rate=0.001, weights_file=None,name='net1',chosenActivation='relu',chosenLoss='CE'
                 ):

        self.num_nodes_in_layers = num_nodes_in_layers


        #include input,hidden,output
        self.no_of_layers=len(num_nodes_in_layers)

        self.batch = batch
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.weights_file = weights_file

        self.w=[np.random.normal(0, 1, [self.num_nodes_in_layers[i], self.num_nodes_in_layers[i+1]]) for i in range(self.no_of_layers-1)]
        self.b=[np.zeros((1, self.num_nodes_in_layers[i])) for i in range(1,self.no_of_layers)]



        self.loss = []

        self.name=name

        self.chosenActivation=chosenActivation
        self.chosenLoss=chosenLoss

        self.aA={
        'relu':[function.relu,function.delReluFromRelu],'sigmoid':[function.sigmoid,function.delSigFromSig],'tanh':[function.tanh,function.delTanhfromTanh]
        }
        self.lF={
        'MSE':function.MSE,'CE':function.cross_entropy
        }
        self.calcLoss=True
        self.applySoftmax=True
        self.applyRegularization=True
        self.regularizationConst=0.01



        #for batch

        self.otherImplementation=True

        self.changeActivation(self.chosenActivation)

        # self.epochs=1
    def saveWeightsBiasJSON(self):
        import json
        w=[i.tolist() for i in self.w]
        b=[i.tolist() for i in self.b]
        with open(self.name+'WB.json', 'w') as outfile:
            json.dump({'weights':w,'biase':b}, outfile)
    def showModel(self):
        print('layers: ',self.num_nodes_in_layers)
        print('learning rate: ',self.learning_rate)
        print('chosenActivation: ',self.chosenActivation)
        print('epochs: ',self.epochs)

    def changeActivation(self,activ):
        [self.activation,self.fasqwdfzeelActivationFromActivation]=self.aA[activ]

    def save(self):
        filehandler = open(self.name, 'wb') 
        pickle.dump(self, filehandler)

    def load(self):

        filehandler = open(self.name, 'rb') 
        return pickle.load(filehandler)

    def lossGraph(self):
        import matplotlib.pyplot as plt
        ypoints = np.array(self.loss)
        xpoints = np.array([i for i in range(len(self.loss))])

        plt.plot(xpoints, ypoints)
        plt.show()

    def activation(self,a):
        return function.relu(a)
    def delActivationFromActivation(self,a):
        return function.delReluFromRelu(a)

    # function.relu
    def feedforward(self,a,activation=function.relu):

        activation=self.activation
        self.fasqwdfzeop=[]
        self.rasqwdfzeopop=[]
        for w,b in zip(self.w,self.b):
            
            self.fasqwdfzeop.append(np.dot(a, w) + b);
            a = activation(self.fasqwdfzeop[-1])

            self.rasqwdfzeopop.append(a);

        return a

    def train(self, inputs, labels):

        self.changeActivation(self.chosenActivation)
        s=time.time()
        for epoch in range(self.epochs):
            it = 0
            while it < len(inputs):

                ib = inputs[it:it+self.batch]
                lb = labels[it:it+self.batch]
                
                self.feedforward(ib)
                y=function.softmax(self.fasqwdfzeop[-1]) if self.applySoftmax else self.rasqwdfzeopop[-1]

                loss=0
                if self.calcLoss:
                    loss = self.lF[self.chosenLoss](y, lb)
                    if self.applyRegularization:
                        loss += function.L2_regularization(self.regularizationConst, self.w)
                    self.loss.append(loss)
                self.fasqwdfze=[(y - lb) / y.shape[0]]



                for i in range(self.no_of_layers-2):
                    pd=self.fasqwdfze[-1]
                    cd=np.dot(pd, self.w[-1-i].T)
   
                    cd*=self.fasqwdfzeelActivationFromActivation(self.rasqwdfzeopop[-1-i-1])
                    self.fasqwdfze.append(cd)


                if self.otherImplementation:
                    for bn in range(self.batch):
                        self.fasdfz=[np.dot(np.array([self.rasqwdfzeopop[-2][bn]]).T, [self.fasqwdfze[0][bn]])]
                        self.fasdfze=[np.sum([self.fasqwdfze[0][bn]], axis = 0, keepdims = True)]
                        for i in range(self.no_of_layers-2-1):
                            self.fasdfz.append(np.dot(np.array([self.rasqwdfzeopop[-3-i][bn]]).T, [self.fasqwdfze[i+1][bn]]))
                            self.fasdfze.append(np.sum([self.fasqwdfze[i+1][bn]], axis = 0, keepdims = True))
                        self.fasdfz.append(np.dot(np.array([ib[bn]]).T, [self.fasqwdfze[-1][bn]]))
                        self.fasdfze.append(np.sum([self.fasqwdfze[-1][bn]], axis = 0, keepdims = True))


                else:
                    self.fasdfz=[np.dot(self.rasqwdfzeopop[-2].T, self.fasqwdfze[0])]
                    self.fasdfze=[np.sum(self.fasqwdfze[0], axis = 0, keepdims = True)]
                    for i in range(self.no_of_layers-2-1):
                        self.fasdfz.append(np.dot(self.fasqwdfzeop[-3-i].T, self.fasqwdfze[i+1]))
                        self.fasdfze.append(np.sum(self.fasqwdfze[i+1], axis = 0, keepdims = True))
                    self.fasdfz.append(np.dot(ib.T, self.fasqwdfze[-1]))
                    self.fasdfze.append(np.sum(self.fasqwdfze[-1], axis = 0, keepdims = True))

                # try:
                for i in range(self.no_of_layers-1):
                    if self.applyRegularization:
                        self.fasdfz[i]+=self.regularizationConst*self.w[-1-i]
                        self.fasdfze[i]+=self.regularizationConst*self.b[-1-i]
                    self.w[-1-i]-=self.learning_rate * self.fasdfz[i]
                    self.b[-1-i]-=self.learning_rate * self.fasdfze[i]

                


                print('=== Epoch: {:d}/{:d}\titeration:{:d}\tLoss: {:.2f} ==='.format(epoch+1, self.epochs, it+1, loss))
                it += self.batch
            # break

        print('=== Time (Training) : {} sec for epoch : {} of input size : {} ===='.format(time.time()-s,self.epochs,len(inputs)))

    def test(self, i, l):

        self.changeActivation(self.chosenActivation)

        s=time.time()
        self.feedforward(i)
        sc=self.fasqwdfzeop[-1]
        pr=function.softmax(sc)
        a = float(np.sum(np.argmax(pr, 1) == l)) / float(len(l))
        print('Test accuracy: {:.2f}%'.format(a*100))
        print('=== Time (Testing) : {} sec ,of input size : {} ===='.format(time.time()-s,len(i)))

        message='Test accuracy: {:.2f}%'.format(a*100)+'\n'+'=== Time (Testing) : {} sec ,of input size : {} ===='.format(time.time()-s,len(i))


        return message

