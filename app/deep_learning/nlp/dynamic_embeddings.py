"""
April 28, 2020 - Meetup - https://www.meetup.com/deep-learning-sf/events/270127611/
DynamicEmbedding: Extending TensorFlow for Colossal-Scale Applications
Cosmin Negruseri

https://arxiv.org/abs/2004.08366
*****************************************************************
Summary notes from paper -

1 of the limitations of word2vec to scale to arbitrary words never seen before is the requirement of a pre-processing
step of needing a dictionary of words whose embeddings must be learned. This limits the model to grow - either
into increasing the dimensionality of the embedding or into handling never seen words.

1) This paper uses a Dynamic Embedding Service (DES) can keep track of global info about a layer such as,
    1) Word frequencies
    2) Avg gradient changes
This can be used to decide when to update an embedding. New system is backward compatible with any gradient descent
optimizers like AdaGrad, Adam, SGD, Momentum

2) Reliability: With DES, the actual model becomes small as most data is saved to BigTable. So it becomes more resilient
to failures due to limited resources.

3) Support for Transfer or Multi-task learning: By taking the embedding data out of TensorFlow, multiple models can
share the same layer, simply by using the same operation name and DES cfg. Model sharing thus becomes a norm rather
than an option.

*****************************************************************
Notes from meetup -
Learning is similar to word2vec where you use softmax layer and dot product logits to predict keywords in context.
They try to predict embeddings.

Big trick in learning word2vec is that instead of full softmax on entire vocabulary, can do some -ve sampling.
This way, size of corpus becomes immaterial.

They have a few tasks - they run their system and compare with seq2seq translation models and word2vec.

Embeddings are sharded by worker.
In normal NN, you have the full model on 1 machine & you do data partitioning.
But here they do model partitioning by embedding in separate cells.


1) Infinitie compute - uses BigTable
2) Flexible gradient descent update
3) Reliability
4) Transfer learning capable
*****************************************************************


"""