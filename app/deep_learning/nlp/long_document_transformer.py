"""
Longformer: The Long-Document Transformer
https://arxiv.org/pdf/2004.05150.pdf

Paper reading meetup on Tue, May 5, 2020

Transformer-based approaches use self-attention, whose CPU & memory usage scale quadratically with the sequence length.
This paper addresses that with longformer, who's attention mechanism scales linearly with sequence length.

This can hence be used on documents with thousands of tokens or longer.
-----

Pre-trained transformer models like BERT have 512 tokens chunk length limit.
Simplest approach truncates the document (common approach for classification)

, or breaks it into chunks of length 512 tokens (can be overlapping), processes each
chunk separately, then combines the activations with a task specific model.

A 3rd approach for multihop & open domain QA tasks uses 2-stage model where 1st stage retrieves relevant docs &
2nd stage is used for answer extraction.

All these approaches suffer from information loss due to truncation or cascading errors due to 2 stages.

In contrast, longformer doesnt truncate or chunk, hence it concatenates the available context and processes in single
pass.

This performs well on character-level language modeling datasets of "text8" and "enwik8".

When pretrained, Longformer consistently outperforms RoBERTa model on long document
tasks and sets new state-of-the-art results on WikiHop and TriviaQA.

Autoregressive or left-to-right language modeling
is loosely defined as estimating the probability distribution of an existing token/character given its
previous tokens/characters in an input sequence.

This task is considered one of the fundamental tasks
in natural language and recent prior work on modeling long sequences using transformers has relied
on this task as their primary evaluation

------------

Training -
Tried to fit the largest window size and sequenceh length that would fit in GPU memory.
But that needed large number of gradient updates to 1st learn the local context before learning to utilize longer
context.

So the paper starts with small window size and sequence length on initial phrases and on subsequent phrases, they double
the window size & sequence  length & half the learning rate.

Kept attention computation in FP32 registers to avoid numerical instability issues and used gradient checkpointing to
reduce memory usage.


"""
