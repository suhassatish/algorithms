"""
The basics: From "A Tutorial on Deep Learning Part 2: Autoencoders, CNNs and RNNs" - Oct 20, 2015
Google Brain

1) The weights in input-to-input matrix U, the hidden-to-hidden matrix W and hidden-to-output matrix
V are fixed.
The weight sharing property makes our network suitable for variable-sized inputs. Eg - stock market
value prediction where each stock's historical data stretches back to different lengths of time.

2) To compute the gradient of the recurrent neural network, we use back propagation through time
(BPTT). BPTT is difficult due to a problem known as vanishing/exploding gradient - the magnitude of
the gradient becomes extremely small or extremely large towards the first or last time steps in the
network.

2b) BPTT vanishing gradient problem can cause optimizer to converge slowly. To speed up training,
 we have to clip the gradient to certain values. Eg: Any dimension of the gradient should be < 1,
 if value of a dimension is > 1, we should set it to be 1.

2c) Reason for vanishing or exploding gradient: Use of sigmoidal activation functions in RNNs.
As the error derivatives are back-propagated, it has to be multiplied by the derivative of the
sigmoid function, which can saturate quickly.

3) In the forward pass, pretend the weights are not shared.

4) In the backward pass, compute the gradient with respect to all W's and all U's. The final
gradient of W is the sum of all gradients for W0;W1; :::;WT ; and the final gradient of U is the sum
of all gradients for U0;U1; :::;UT.
------------------------------------------
LSTM : Long Short-Term Memory Recurrent Networks:

Key idea: Modify the architecture of RNN to allow the error derivatives to flow better.

LSTM/ GRU (gated recurrent unit) cells  - let the gradient flow.
vanilla RNN replaced with LSTM.
GRU is more recent (3 years ago).
GRU is a gating mechanism in recurrent neural networks introduced in 2014.
Their perf on polyphonic music modeling and speech signal modeling was found to
be similar to LSTM. They have fewer parameters than an LSTM as there's no output gate.

Application: deep speech
"""