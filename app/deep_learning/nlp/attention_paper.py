"""
https://arxiv.org/pdf/1409.0473.pdf
2015 - Bengio - [1409.0473] Neural Machine Translation by Jointly Learning to Align and Translate (main attention paper)

NMT has so far relied on encoder-decoder architecture where encoder encodes a sentence into a fixed length vector
from which a decoder generates a translation. In this paper, we argue that the fixed length vector is a bottleneck.

It encodes the input sentence into a sequence of vectors of different sizes and then chooses a subset of these vectors
adaptively while decoding the translation. This allows the model to cope better with longer sentences.


"""