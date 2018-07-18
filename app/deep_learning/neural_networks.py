# -*- coding: utf-8 -*-
"""
-------
Back propagation:
In back propagation of the error function, a general method for non-linear optimization called
"gradient descent" is applied. The network calculates the derivative of the error function with
respect to the network weights, and changes them to decrease the error (thus going downhill on the
surface of the error function).
For this reason, back-propagation can only be applied on networks with differentiable activation
functions.

--------
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
More on RELu (rectified linear unit): This is a function defined as y = x for x >=0 and 0 for x < 0
Properties  -
1) Not differentiable at a single point x = 0. We can still use sub-derivatives. We can use
sub-gradient descent to optimize such functions.
  (Aside from wikipedia - https://en.m.wikipedia.org/wiki/Subderivative?wprov=sfla1
  In maths, sub-derivative, sub-gradient and sub-differential generalize the derivative to functions
  which are not differentiable. In a convex function with a sharp angle, the tangent at the bend
  are several lines with different slopes. The slope of such a line is called SUB-DERIVATIVE.
  The set of all sub-derivatives is called the SUB-DIFFERENTIAL. If function f is convex and its
  sub-differential at x0 contains exactly one sub-derivative (line), then f is differentiable at x0.
  )

Why dont we use the soft-plus rectifier (y = ln(1 + e**x)) instead of RELU?
  (Aside from wikipedia - https://en.wikipedia.org/wiki/Rectifier_(neural_networks)
  Rectifier is an activation function defined as f(x) = max(0, x) where x = input to neuron
  Soft-plus is the smooth approximation to the ReLU rectifier
  )

2) Computationally very cheap

3) Offers sparsity - Sparsity improves signal-to-noise ratio because weak responses are thresholded
out.
    Reasons 2) and 3) are advantages over soft-plus.
    Also, according to Ian Goodfellow, 2) and 3) are not bottlenecks in DNNs since most computation
    bottlenecks are concentrated in matrix operations and not the activation evaluations.

4) Simple derivatives. d/dx = 1 for x > 0 and 0 elsewhere. This is very important for efficient
    gradient propagation in very deep neural networks (DNNs)
-----
Variations of ReLU -
1) Noisy ReLU - defined as y = max(0, x + Y ) with Y = normal distribution with mean = 0, σ(x)
    They have been used with some success in restricted boltzmann machines for computer vision tasks

2) Leaky ReLU - f(x) = x if x > 0; 0.01x otherwise

3) Parametric ReLUs take this even further with definition
    f(x) = x if x > 0; ax otherwise
    with a being a learned parameter along with other neural network parameters.
    For a <= 1, f(x) = max(x, ax). Has a relation to "maxout" networks.

4) Exponential Linear Units (ELU) - Try to make activations closer to zero which speeds up learning.
ELUs have obtained greater classification accuracy than ReLUs.
f(x) = x if x >=0 and a(e**x - 1) otherwise,
where a is a hyper-parameter to be tuned with the constraint a >= 0
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
---
8)
If P_dropout = probability of dropout where an entry in the neural network node weight matrix W_ij is 0,
then h_drop = γ * d * h where d = d-dimensional vector of 0s and 1s such that an entry d_i = 0 with P_drop and
    d_i = 1 with probability (1 - P_drop)

γ can be derived to be = 1 / (1 - P_drop)

----------------------------------------------------------------
Minimize model complexity -
Thumb rules:

1)
you shouldn't have more than 2F the number of nodes to features in your 1st layer of NN,
if the features are highly uncorrelated. If they are somehow correlated, you should keep
number of nodes N = 0.5F.
Therefore 0.5F <= N <= 2F

2) Most data scientists only have about 10s of thousands of labeled training samples.
Total number of weights in your hidden layers = max (0.5 * total number of training samples)
You can trick this rule a bit with droupout, but thats about it.

3) Keep an eye out for training error vs test error.
----------------------------------------------------------------

INITIALIZING WEIGHTS IN A NEURAL NETWORK:
In order to minimize neurons becoming too correlated and ending up in a poor local minima,
its often helpful to randomly initialize the parameters. One of the frequent initializations used is called XAVIER
INITIALIZATION. It states that given a matrix A of m x n dimension, select values A_ij uniformly from [-ε, ε]
where ε = sqrt(6) / sqrt(m + n)

"""