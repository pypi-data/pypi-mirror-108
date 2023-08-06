
  
import numpy as np
def relu(inputs):
    return np.maximum(inputs, 0)
def delRelu(rel):
    return int(rel>=0)



def delReluFromRelu(rel):

    return np.vectorize(delRelu)(rel)


# def sigmoid()
def sigmoid(a):
    return 1/(1+np.exp(-a))


def delSigmoid(a):
    sig=sigmoid(a)
    return sig*(1-sig)


def delSigFromSig(sig):

    return sig*(1-sig)


def tanh(a):
    return np.tanh(a)

def delTanhfromTanh(ta):
    return 1-ta*ta

def softmax(inputs):
    exp = np.exp(inputs)
    return exp/np.sum(exp, axis = 1, keepdims = True)

def cross_entropy(inputs, y):
    indices = np.argmax(y, axis = 1).astype(int)
    probability = inputs[np.arange(len(inputs)), indices] 
    log = np.log(probability)
    loss = -1.0 * np.sum(log) / len(log)
    return loss

#mean squared error
def MSE(inputs,y):
    return np.sum((inputs-y)**2)/len(y)

# L2 regularization
def L2_regularization(la, weight):
    return np.sum([0.5 * la * np.sum(w*w) for w in weight])
