"""
deepgram kur tutorial by Adam

//mnist.yaml setting - can run on tensor flow, pyTorch or keras; keras doesn't run in multi-gpu mode;
//it prefers tensorFlow if installed, if found; else , uses the library thats packaged within its git repo = keras

settings:
  backend:
    device: gpu
    parallel: 4

Neural networks are non-deterministic, so a bad initialization can result in poor accuracy. Re-training usually fixes
the issue
---------
DeepSpeech -
Sorta Grad - improving training stability.
Sort samples by utterance length in the first epoch, then fall back to regular SGD.

batch normalizations -reducing internal covariance shift (internal activations)

LSTM/ GRU (gated recurrent unit) cells  - let the gradient flow.
vanilla RNN replaced with LSTM.
GRU is more recent (3 years ago).
GRU is a gating mechanism in recurrent neural networks introduced in 2014.
Their perf on polyphonic music modeling and speech signal modeling was found to
be similar to LSTM. They have fewer parameters than an LSTM as there's no output gate.


Make your model easier to optimize before scaling.
Pick the model that is easier to scale.
If 5 layer is good enough, then dont go for 7 layers.
Try to reduce learning rate.

Skip-layers or residual nets are fancy techniques while computing back-prop.
huangjiaji@baidu.com  (PhD, May 2016. Hired by Baidu @ NIPS. Researh in statistical
signal processing)

Melanox is the only company in the World that does distribution of deep learning
models across GPUs that can talk to each other. 10 Gbps = best in class N/w B/W

Melanox N/W cards are 50-100 Gbps. For baidu to train these models in parallel,
Baidu has to rely on melanox.
Typically 16-32 GPUs training on web scale data.
------------------------------
Jonathan Hseu - Google Brain SWE/Manager - Tensor Flow

slides link to talk -
https://docs.google.com/presentation/d/1fWZn-_vFrEi05Cjh0iwc7T1NBQM5aNwcvkpJq3LW-is/edit?ts=58d6e9bf#slide=id.g1d4ba00721_0_0

TensorFlow - #1 repo for ML on GitHub. #1 for any non-javascript tutorial.
Open source models -
github.com/tensorflow/models

Applications -
Diabetic retinopathy
skin cancer detection
dog breed distinction - between Alaskan malamute and Siberian Huskie
text summarization - getting training data is hard, since newspaper headlines are misleading.
neural machine translation - uses model parallelism; data parallelism is easier.
neural architecture search - use reinforcement learning to come up with NN architectures; ton of cnxns looks like ResNet
alternative RNN set, works better than LSTMs.

TensorFlow Design -
TF separates computation graph construction from execution.
c = tf.add(a,b)
all nodes are ops. constants, variables, debug code (print, assert), control flow

with special functions for deep learning - matmul, reduce_sum
Some ops are stateful. Must be initialized. adta type of a tensor is fixed (homogenous) but shape is not.

Tolerable upper bound for training = 1-2 weeks.
Adding 100ms to someone's search query due to search ranking bottle-neck is not acceptable.

Team magenta works on music and art at Google.

Udacity class done by someone on Google Brain team-
goo.gl/iHssll

Fun experiments -
Deep dream - goo.gl/OCYseb
Style transfer - goo.gl/fyDxhC
image completion - goo.gl/67hfSo

XLA- most exciting new feature of TF - Linear Algebra ops hardware optimized
- Can Implement 1 class defining 50-100 linear algebra ops.
Makes H/W more competitive. U can fuse ops, makes model faster. Syntax net inference is 200X faster.
"""