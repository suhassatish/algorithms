"""
Quora answer by an Applied Scientist at Amazon.com
Deep Learning frameworks operate at 2 levels of abstraction:

Lower Level: This is where frameworks like Tensorflow, MXNet, Theano, and PyTorch sit. This is the
level where mathematical operations like Generalized Matrix-Matrix multiplication and Neural Network
primitives like Convolutional operations are implemented.

Higher Level: This is where frameworks like Keras sit. At this Level, the lower level primitives are
used to implement Neural Network abstraction like Layers and models. Generally, at this level other
helpful APIs like model saving and model training are also implemented.

You cannot compare Keras and Tensorflow because they sit on different levels of abstraction.
------------------------
Keras -
1) Useful for applications beyond just deep learning.
2) Beautifully  written functional API, that gets out of your way for more exotic applications.
3) Keras does not block access to lower level frameworks.
4) Keras results in much more readable and succinct code.
5) Keras model Serialization/Deserialization APIs, callbacks, and data streaming using Python
generators is very mature.
6) Keras has been declared the official high level abstraction for Tensorflow.

PyTorch -
Dynamic graph of PyTorch makes it really easy to handle variable length sequences.

"""