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
"""