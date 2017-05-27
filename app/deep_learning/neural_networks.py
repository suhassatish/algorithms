"""
Ian Goodfellow's answer on Quora to the question:

Q) Why are autoencoders considered a failure?
A) Autoencoders are useful for some things (like?) but not nearly as useful as once thought.
For training deep nets, the thinking 10 years ago (~ in 2007) was that if trained with only
back propagation of the supervised cost, they may not learn correctly. So they may also need an
unsupervised cost, like the autoencoder cost to regularize them.

When Google Brain built their first very large neural network to recognize objects in images,
it was an autoencoder. It didn't work very well at recognizing objects compared to later approaches.
Today, we can recognize objects  very well just by using back propagation of the supervised cost,
as long as there is enough labeled data.
----------------------------------------------------------------
Ian Goodfellow's answer on Quora to question - Where is sparsity important in deep learning?

Each unit in a neural network should usually be connected to relatively few other units.
The human brain has 1e10-1e11 neurons, but each neuron is only connected on an avg to 1e4 neurons.
In ML, convolutional neural networks (CNNs) follow this pattern, where each unit receives inputs
from only a very small patch in the layer below.

Fully connected network with zero weights in most places is similar to a sparesely connected
network with mostly non-zero weight connections. Sparsity of connections is better though, since
you dont pay the computational cost of multiplying with zero and adding up a bunch of zeros.

1) So far, learning weights that are sparse hasn't really paid off.
2) Learning activations that are sparse doesn't really seem to matter either.
3) 5 years ago, people thought RELU worked well as they were sparse, but the actual reason is they
were piece-wise linear. Max-out (dense N/W) can beat RELU in some cases, and performs the same as
RELU in other contexts, but its not sparse at all.
----------------------------------------------------------------
http://proceedings.mlr.press/v28/goodfellow13.pdf
Notes from Ian Goodfellow's research paper on Maxout networks -

1)
Dropout is an inexpensive method to train a large ensemble of models that share parameters and
approximately average together these models' predictions.

2) Dropouts applied to multi-layer
perceptrons and deep CNNs have improved the state of the art on tasks ranging from audio
classification to very large scale object recognition.

3)
Dropout is viewed as an indiscriminately applicable tool that reliably yields modest improvement
in performance when applied to almost any model.

4) Dropout is most effective when taking relatively large steps in parameter space.

5) Dropout can be used to reduce over-fitting of your model. What dropout does is getting randomly
rid of some of your data, adding null noise to the samples. In this way, the model will be able to
memorize only random sections of each sample, therefore it will be forced to generalize in order to
get a good prediction accuracy.

6) A 0.5-0.75 dropout rate between fully connected layers is going to
work quite well and a 0.1-0.3 dropout rate would typically do better for the input layer.

7) The more data you have, the less drouput you actually need.
----------------------------------------------------------------
Minimize model complexity -
Thumb rules:

1)
you shouldn't have more than 2F the number of nodes to features in your 1st layer of NN,
if the features are highly uncorrelated. If they are somehow correlated, you should keep
numbe of nodes N = 0.5F.
Therefore 0.5F <= N <= 2F

2) Most data scientists only have about 10s of thousands of labeled training samples.
Total number of weights in your hidden layers = max (0.5 * total number of training samples)
You can trick this rule a bit with droupout, but thats about it.

3) Keep an eye out for training error vs test error.
"""