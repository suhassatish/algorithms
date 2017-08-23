"""
TODO -
http://cs231n.github.io/convolutional-networks/
Stanford Course (open source) on Convolutional neural networks for Visual Recognition

1) ConvNet Layers:
  a) Convolutional layer
  b) Pooling layer
  c) Normalization layer
  d) Fully-connected layer
  e) Converting fully-connected layer to convolutional layer

2) ConvNet Architectures:
  a) Layer patterns
  b) Layer sizing patterns
  c) Case studies - LeNet, AlexNet, ZFNet, GoogleNet, VGGNet

3) Computational considerations

-----------------------
TODO -
http://blog.christianperone.com/2015/08/convolutional-neural-networks-and-feature-extraction-with-python/
---------
The basics: From "A Tutorial on Deep Learning Part 2: Autoencoders, CNNs and RNNs" - Oct 20, 2015
Google Brain

1) CNNs are not fully connected, ie every neuron is not connected to every neuron in the previous
layer. Training with gradient descent is possible because we can modify the back-propagation
algorithm to deal with local connectivity.

2) The max pooling layer in the convolutional neural networks is also known as the subsampling layer
because it dramatically reduces the size of the input data.

3) Conv-nets with max-pooling result in translational invariance, ie 2 similar images with a few
pixels that have moved slightly are still treated as the same.

4) Some recent convolutional neural networks achieve brightness invariance by using an extra layer
on the o/p of max-pooling layer called Local Contrast Normalization (LCN).

5) Some library implementations (like in MATLAB) may convert the convolution step to an FFT
operation for fast computation.
"""