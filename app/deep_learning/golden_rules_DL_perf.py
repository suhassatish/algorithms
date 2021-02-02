"""
Jun 20, 2020 - 10 am to 1 PM - PyTorch Fundamentals - Ravi Ilango Sr Data Scientist

Typical nlp pipeline: ~/Dropbox/Tech_extras/nlp/nlp-pipeline.png

Sentence segmentation -> tokenization -> POS, lemmatization -> dependency parsing -> named entity recognition ->
stop words -> noun phrases -> coreference resolution -> data structures

Transformer networks are parallelizable during training while LSTMs are not. Hence LSTM is getting phased out
in production in favour of transformer networks, BERT, etc.

GPT2Tokenizer is another model pre-trained using Transformer networks.
---------------------------------------

Golden rules of deep learning performance - https://www.youtube.com/watch?v=ZAHaVuwqw2I

1)
Use 16-bits to store weights. Put this at the top of your training code file
os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'
automatic mixed precision

2) use larger batch size.

3) 5X increase in throughput by changing the batch size from 4095 to 4096
Use multiples of eight - like channels in convolutional filter, size of mini-batches, etc.

Otherwise, instead of specialized tensor cores from Nvidia, it falls back to GPUs.
Most optimal perf for Nvidia, use multiples of 64 or 256 recommended.

Google TPU - use multiples of 128.

4) find the optimal learning rate.
    use keras_lr_finder library

5) use @tf.function on top of a function for graph-based execution like TF1.0. Benefit from speedup of graph based exe
without giving up eager exeuction benefits of TF2.0.

6) overtrain and then generalize.
    progressive sampling
    progressive augmentation
    progressive resizing
            seen in fast.ai
            half height & width = 75% less data = 4X speedup
            quarter height and width = 16X speedup
            small resolution = force learning high level details, broad shapes, colors
            then higher resolution fine tuning

7) install an optimized stack for the hardware
    hosted binaries are built to run on range of hardware
    building TF manually with your machine's instruction set

8) optimize number of parallel CPU threads
    exploit parallelism between different operations
    tf.config.threading.set_intra_op_parallelism_threads(num_threads)

9) Need 10M input data size to match human performance. Need atleast 5K input samples per output class for good perf.
"""