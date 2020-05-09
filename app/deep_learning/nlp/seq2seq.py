"""
2014 - Google - [1409.3215] Sequence to Sequence Learning with Neural Networks (seq2seq)
https://arxiv.org/pdf/1409.3215.pdf

SGD could learn LSTMs that had no trouble with
long sentences. The simple trick of reversing the words in the source sentence is one of the key
technical contributions of this work.

A useful property of LSTM is that it maps sentences of differing lengths to a fixed dimensional vector repr.

Deep LSTMs with 4 layers significantly outperform shallow LSTMs.

"""