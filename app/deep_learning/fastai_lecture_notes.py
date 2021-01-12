from torch import exp

"""
Notes from 2020 version of fast.ai lectures and book notes

https://docs.fast.ai/

https://github.com/fastai/fastbook

~/Dropbox/tech_extras/deep_learning/DL-4-coders-fastai-PyTorch-AI-apps-JeremyHoward-2020.pdf

********************************************************************************

LECTURE 1 - https://colab.research.google.com/github/fastai/fastbook/blob/master/01_intro.ipynb#scrollTo=S4JPxWbL9pND

1) Training resNet34 model on cat and dog breeds images from Oxford-IIIT Pet Dataset
resnet34 has been pretrained on 1.3M images of ImageNet dataset.
We are using transfer learning to help it learn cat & dog breeds.

The 34 in resnet34 refers to the number of layers in this variant of the architecture
(other options are 18, 50, 101, and 152). Models using architectures with more layers take longer to train, and are
more prone to overfitting (i.e. you can't train them for as many epochs before the accuracy on the validation set starts
 getting worse). On the other hand, when using more data, they can be quite a bit more accurate.

When using a pretrained model, cnn_learner will remove the last layer, since that is always specifically customized to
the original training task (i.e. ImageNet dataset classification), and replace it with one or more new layers with
randomized weights, of an appropriate size for the dataset you are working with. This last part of the model is known
as the head.

It is not yet well understood how to use transfer learning for tasks such as time series analysis.

learn.fine_tune(1) - this lib function is used to fit pretrained models for 1 epoch, using learn.fit() will throw away
the pretrained weights and randomly initialize them.

Segmentation - Definition - Creating a model that can recognize every single pixel in an image

learn.fit_one_cycle(3) - most commonly used method for training fastai models from scratch
Sometimes it's best to experiment with fine_tune versus fit_one_cycle to see which works best for your dataset.
Saves intermediate model results but fine_tune() doesnt.

TRAINING DATASET VS VALIDATION DATASET VS TEST DATASETS in practice -
if you're considering bringing in an external vendor or service, make sure that you hold out some test data that the
vendor never gets to see. Then you check their model on your test data, using a metric that you choose based on what
actually matters to you in practice, and you decide what level of performance is adequate.

********************************************************************************

Lecture 2 - PRODUCTION

Think out of the box. Sound dataset can be converted into an image dataset by converting their acoustic waveforms into
images and training a CNN model on them.

The ability of deep learning to combine text and images into a single model is, generally, far better than most people
intuitively expect.

A deep learning model can be trained on input images with output captions written in English

For time series and tabular data, DL has been making great strides but still in early stages. Its used as an ensemble
along with traditional ML models. DL makes it easier to use natural language text inputs as well as high-cardinality
input features such as zip codes.

Downside is training takes longer.

Open source projects like https://rapids.ai/ bring GPU power to traditional algorithms like XGBoost.
See how to use rapids.ai to deploy an ml-flow app on GKE here -
https://medium.com/rapids-ai/an-end-to-end-guide-to-hyperparameter-optimization-using-rapids-and-mlflow-on-gke-8c07596cfff5
(written Dec 15, 2020)

Bing image search is the best as of Dec 2020 and the API can make 1K requests per month with each request able to
download upto 150 images.

BING search API call in python example -
https://github.com/Azure-Samples/cognitive-services-REST-api-samples/blob/master/python/Search/BingWebSearchv7.py

Common data augmentation techniques for images - rotation, flipping, perspective warping, brightness and contrast changes

fastai lib's aug_transforms performs pretty well

To tell fastai we want to use these transforms on a batch, we use the batch_tfms parameter.

********************************************************************************
LECTURE 3 - bias in AI, skipped

LECTURE 4 - MNIST hand written digit image classification

In pytorch, any method that ends in an underscore means the tensor operation happens in-place.

Small neural nets with lesser hidden layers have large matrices with expensive matrix ops but large number of hidden
layers have smaller matrices and are hence computationally more efficient.
"""
import torch


def mnist_loss(inputs, targets):
    """
    :param inputs:
    :param targets:
    :return: list of indices where the function is true in the tensor
    """
    inputs = inputs.sigmoid()
    return torch.where(targets==1, 1-inputs, inputs).mean()


"""
********************************************************************************

LECTURE 5 - pet breeds
https://github.com/fastai/fastbook/blob/master/05_pet_breeds.ipynb

fastai default loss function for image data and a categorical outcome is cross-entropy loss.
This loss function works for multi-class classification as well, and results in faster and more reliable training.

x,y = dls.one_batch()
gives 1 batch of data from a data loader
"""
def softmax(x): return exp(x) / exp(x).sum(dim=1, keepdim=True)


"""
Softmax is the multi-category equivalent of sigmoid activation function.
Probability of categories must add upto 1.

Cross-entropy loss = max log likelihood of softmax.

For 10 MNIST digits, we pick the loss from the column containing the correct digit.

pytorch function nll_loss (NLL stands for negative log likelihood) but its a misnomer and doesnt take the log at all.
Its supposed to be used after log_softmax which combines log and softmax in a fast and accurate way. 

nn.CrossEntropyLoss() === nll_loss(softmax(..)) === F.cross_entropy(activations, target_label)
By default PyTorch loss functions take the mean of the loss of all items. You can use reduction='none' to disable that:
    nn.CrossEntropyLoss(reduction='none')(acts, targ)
    
Taking the logarithm is useful to convert a probability between 0 and 1 to a scale of -Infinity to +Infinity. This
helps disambiguate a model with 0.999 confidence on a prediction from another prediction with confidence of 0.99. 
1 of them is 10 times more confident than the other but when rounded, both yield 1. 

Gradient of softmax(a, b) = softmax(a) - b

Default learning rate is 1e-3 in fastai lib. Double the learning rate in each epoch until you see an increase in error. 
The lr @ which error increased / 10 should give you the best learning rate. 

DISCRIMINATIVE LEARNING RATE - different layers of a pretrained model have different learning rates. The last layer aka
head, needs a higher learning rate than the deepest layers. This was 1st developed in ULMFiT approach to NLP transfer
learning. 

HOW TO CHOOSE NUMBER OF EPOCHS TO TRAIN FOR?
1) See how much time you're willing to train for, and train for that long and see how long each epoch took. 
2) Plot training_loss, validation_loss, your metrics ( like accuracy or error_rate) and time. 
3) If your model has overfit as seen from the plot, throw away the trained model and retrain from scratch, by now
choosing the number of epochs as the # at which the model started overfitting (ie the validation loss  or error 
increased)

EARLY STOPPING, ie the weights checkpoint snapshot at the end of each epoch are unlikely to give you the best model
because they are from a point when the learning rate has not become really small where it can find the best result.

4) If you have more time to train, then use a deeper architecture with more layers. Eg, if you're using resnet18, try 
resnet50.

5) Deeper model needs more GPU RAM, so reduce the batch size.
  
6) If larger model training takes a long time, try using MIXED_PRECISION TRAINING, ie Learner(..).to_fp16() in fastai. 
This uses Nvidia's GPU feature called TENSOR CORES, that can dramaticaly speed by training by 2-3X.

7) Freeze weights of a pre-trained model and change the head (final layer) to randomized weights for the task at hand.
Specify number of epochs, M to train with frozen weights which will only modify the randomized weights of the HEAD. 
After those epochs, unfreeze weights and train all layers for N epochs. M and N can be hyper-parameters to your model.
 
********************************************************************************
LECTURE 6 - https://github.com/fastai/fastbook/blob/master/06_multicat.ipynb

Most likely you will need the follow loss functions for the following kinds of problems - 
The model can be the same but with different number of outputs in the final layer accordingly, with the below loss fns - 

pandas dataframe rows and cols can be accessed with the method
df.iloc[0, :] 

creating a pandas DF - 
tmp_df = pd.DataFrame({'a':[1,2], 'b':[3,4]})

DATASET:: A collection that returns a tuple of your independent and dependent variable for a single item
DATALOADER:: An iterator that provides a stream of mini-batches, where each mini-batch is a tuple of a batch of 
independent variables and a batch of dependent variables

DATASETS:: An object that contains a training Dataset and a validation Dataset
DATALOADERS:: An object that contains a training DataLoader and a validation DataLoader

Python lambda functions dont serialize, so bad for production code but good for prototyping in jupyter notebooks.

PyTorch's F.binary_cross_entropy and its module equivalent nn.BCELoss calculate cross-entropy on a one-hot-encoded 
target, but do not include the initial sigmoid.
Normally for one-hot-encoded targets you'll want F.binary_cross_entropy_with_logits (or nn.BCEWithLogitsLoss), 
which do both sigmoid and binary cross-entropy in a single function


----------
Summary - 
for single-label classification
    F.cross_entropy or  nn.CrossEntropyLoss is the version with softmax included
    F.nll_loss or nn.NLLLoss is the version w/o softmax
     
nn.BCEWithLogitsLoss for multi-label classification (BCE = binary cross entropy)
nn.MSELoss for regression 

********************************************************************************
LECTURE 7 - Sizing and TTA ie test time augmentation
https://github.com/fastai/fastbook/blob/master/07_sizing_and_tta.ipynb

Thumb rule - sample dataset to a small enough size to be able to iterate on ideas in under 2 mins during development.

Useful techniques for images - 
1) NORMALIZATION - mean 0 and std-dev = 1. Really important Tx for pretrained models.
    If no statistics are passed to normalize function, fastai will calculate it from 1 batch of data.
     
2) PROGRESSIVE RESIZING - Start training on a smaller sized image and then slowly grow the image size.
For transfer learning from pretrained models, this may actually HURT perf. 
    a) This is most likely to happen if your pretrained model was quite similar to your transfer learning task and 
    dataset and was trained on similar-sized images, so the weights don't need to be changed much. In that case, 
    training on smaller images may damage the pretrained weights.

    b) On the other hand, if the transfer learning task is going to use images that are of different sizes, shapes, 
    or styles than those used in the pretraining task, progressive resizing will probably help. 
    As always, the answer to "Will it help?" is "Try it!"

3) TEST TIME AUGMENTATION - Augmentations such as random cropping, resizing, rotations, flipping, but on validation set.
    During inference or validation, creating multiple versions of each image, using data augmentation, and then taking 
    the average or maximum of the predictions for each augmented version of the image.
    
    Advantages - With same training time, accuracy can improve dramatically.
    Disadvantage - Makes inference slower.
    
    Fastai defaults to unagmented center-crop image + 4 randomly augmented images.

4) MIXUP - its a powerful data augmentation technique. For each image undergoing augmentation,
    take weighted avg of image and a random image from dataset with a random weight. Thats your perturbed new image.
    
    Advantages - Dramatically higher accuracy if you dont have pretrained models similar to your domain's data.
    
    Callbacks are what is used inside fastai to inject custom behavior in the training loop
    
    Mixup used inside activations in models can also improve NLP tasks.
    
5) LABEL SMOOTHING - Replace 0 labels with a 0 + ε/N and 1 label with 1 - ε/N where N is the #(classes), 
    so that training doesnt become over-confident.
    1-hot encoding is seldom done in practice, since its memory-intensive.
    
    Like with Mixup, you won't generally see significant improvements from label smoothing until you train more epochs. 
    
********************************************************************************

LECTURE 8 - COLLABORATIVE FILTERING - movie lens dataset

1) Randomly initialize a set of LATENT FACTORS for each User and Movie. Genres such as sci fiction, old movies, action,
    can be the latent factors. Each user can be represented as a weighted vector for their preference to these latent
    factors being the weights in [-1, 1]. This approach to recommender systems is called probabilistic matrix 
    factorization (PMF).

2) EMBEDDING - Multiplying by a one-hot-encoded matrix, using the computational shortcut that it can be implemented by 
    simply indexing directly. The thing that you multiply the one-hot-encoded matrix by (or, using the computational 
    shortcut, index into directly) is called the embedding matrix. 

    Take gradient of the loss with respect to the embedding vectors, ie dot product of user_embedding dot movie_embedding
    minus the label. Then update the embeddings to minimize loss with the SGD or other optimizer.

3) WEIGHT DECAY - aka L2 regularization in a movie lens data set context, takes the norm(weights) ie Σ w_i**2
   loss_with_weight_decay = loss + weight_decay * (parameters**2).sum
   
   Since d/dx (x**2) = 2x, we have the gradient parameters.grad += 2 * wd * parameters
    where wd = weight_decay

4) Interpretation of movie_bias - 
    Low bias => even when the latent vector of a movie closely matches a user's taste,
        they dont like it, ie labeled rating is low. 
        
    High bias => Even when latent vector is not a match at all to a user's taste of genre for ex, they tend to like it.
    Eg - silence of the lambs is liked by someone who doesnt like horror
    
5) Interpreting the embedding matrix is not easy. We can adopt PCA.

6) Cold start bootstrapping == biggest problem, ie when there are no reviews or ratings. To address - 
    a) Can assign new users mean of embedding vectors of all users
    b) Or ask users some questions when they sign up, eg - flixster.
    c) watch out for bias, eg - anime lovers are a vocal minority who punch their weight and rate a lot of animes highly
    
********************************************************************************

LECTURE 9 - Tabular Data

1) Random forest doesnt need any normalization or scaling of features. Random forest by itself isnt prone to overfitting
but if its using Xgboost or some boosting where successive models are learnt on errors from previous models, they have
a tendency to overfit.

sklearn's HistGradientBoostingRegressor provides excellent performance.  GBMs have a lot of hyperparams to tune.

Recommend starting with random forest to get a baseline, then use feature importance from it and then try GBM and NNs.
If RFs work well, try adding embeddings for categorical variables.

********************************************************************************

LECTURE 10 - NLP

1) ULMFit (universl language model fine tuning paper from fastai) - Key idea - A LM pretrained on a different corpus
can be fine-tuned by training with few examples from the real transfer learning dataset and then replacing the last 
layer (HEAD) with a classifier can really boost performance. 

2) Default English tokenizer in fastai uses spaCy lib. 

3) BOS = std NLP acronym for beginning of stream

4) Languages like Chinese and Japanese dont have any spaces b/w words, they dont even have a well defined concept of a
    word. Languages like Turkish and Hungarian merge many words together resulting in really long words with contextual
    meaning. SUB_WORD tokenization works well for these scenarios. It works as follows - 
    a) Analyze corpus for most commonly occuring groups of letters. These become the vocab,
    b) Tokenize the corpus using this vocab of sub-word units.
    
    Large sub-word size => almost all words get into the vocabulary
        a) Fewer tokens per sentence
        b) faster training
        c) less memory
        d) less state for model to remember
        e) larger embedding matrices which require more data to learn
        f) can easily scale between character tokenization (ie subword(26) for english) vs word tokenization (subword(10K))
        g) handles every human language w/o lang-specific algorithms to be developed. Can also handle MIDI music 
            notation and genomic sequences.

7) NUMERICALIZATION - converting tokens to integers. Treat the vocab as categorical variables in a list and replace the
    token with its index in the list. Optimizations for keeping embedding matrix small - min_freq =3, max_vocab_size=60K
    ie, replace any word with frequecy 1 or 2 and any word not in 60K size vocab with the unk token 

8) Transfer learning HEAD replacement for LMs in RNN context entails randomly initializing embedding weights for new 
words in target dataset's vocabulary which are not part of the pretrained dataset's vocabulary.
The model not including the final layer which converts the activations into probabilities of picking each token in our
vocabulary as the next word, is called ENCODER.

9) A language model predicts the next word of a document, so it doesn't need any external labels

10) PyTorch DataLoaders need to collate all the items in a batch into a single tensor, and a single tensor has a fixed 
shape.

11) Sort the documents by length prior to each epoch such that documents collated into a batch will be of similar length

12) We won't pad every batch to the same size, but will instead use the size of the largest document in each batch as 
the target size.

13) 11 & 12 above are done automatically by fastai in the TextBlock call with is_lm=False. This is only for the last
classifier stage. For the LM, all documents are concatenated together and then chunks of sentences are batched 
together of equal size.

14)  In computer vision we often unfreeze the model all at once, but for NLP classifiers, we find that unfreezing a few 
layers at a time makes a real difference. (refer to discriminative learning rates above)

15) By training another model on all the texts read backwards and averaging the predictions of those two models, 
we can get to even higher accuracy

********************************************************************************

LECTURE 11 - Data Munging with fastai's Mid-Level API

1) Mid-level API (below the data block API) has a callback system to customize the training loop & optimizer any way we
 like. 

2) Transform class is the parent of Numericalize and Tokenize and always gets applied on a tuple(input, target)       

********************************************************************************

LECTURE 12 - NLP DEEP DIVE

Sequence prediction of next number in sequence in dataset of numbers, training on window size of 3. 
3 linear layers.
1st layer = 1st word's embeddings as activations
2nd layer will use 2nd word's embeddings + 1st layer's o/p activations
3rd layer will use 3rd word's embeddings + 2nd layer's o/p activations

RNN cheat sheet - https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks

To remove all the gradient history in pyTorch (ie keep only the last 3 layers of gradients to avoid vanishing or
exploding gradients problem during back prop thru time in RNNs), use the detach() method.

GRUs and LSTMs try to solve exploding activations in RNNs.

LSTM - keeps 2 hidden states. Hidden state h focuses on next word to predict while cell state c keeps track of what 
happened earlier in the sentence, eg - the subject or proper noun so that the pronoun like he/she can be predicted in 
future.

LSTM INTUITION - 
1) We stack together the input X and hidden state H into 1 big tensor (unlike in RNN where we add them in a linear layer)
 => If n_in is the dimension of i/p X & the embeddings, and n_hid is dimension of hidden layer, dimension of LSTM takes
 n_in + n_hid as input and output is of dimension n_hid.
 
2) The cell state is multiplied with this big tensor which lets the N/W forget things close to 0 and remember things 
close to 1. So when a period  or xxbos end of sentence character is detected, the LSTM forgets state before starting
the next sentence. 

3) For instance, we may see a new gender pronoun, in which case we'll need to replace the information about gender that
 the FORGET GATE removed.

4) INPUT GATE decides which elements of the cell state to update.  

5) The THIRD GATE determines what those updated values are, in the range of –1 to 1 (thanks to the tanh function)

6) The last gate is the OUTPUT GATE determines which information from the cell state to use to generate the output. 

7) More efficient to compute 1 big matrix mult on GPU than 4 smaller mults.

8) LSTMs are still prone to overfitting. Data augmentation can mitigate this but needs another N/W to do the data 
augmentations. Effective use of dropout, activation regularization, and temporal activation regularization could allow 
an LSTM to beat state-of-the-art results.

9) ACTIVATION REGULARIZATION is often applied on dropped out activations while TEMPORAL ACTIVATION REGULARIZATION is 
applied on non-dropped-out activations.

Conclusion - The AWD-LSTM architecture employs - 
    a) Embedding dropout (just after the embedding layer)
    b) Input dropout (after the embedding layer)
    c) Weight dropout (applied to the weights of the LSTM at each training step)
    d) Hidden dropout (applied to the hidden state between two layers)

********************************************************************************
https://www.fast.ai/2018/07/02/adam-weight-decay/
AdamW and Super-convergence is now the fastest way to train neural nets
Adam optimizer basic ideas - 
1) Why use the same learning rate for every param when we know some move faster than others?

2) Square of gradients tells how much signal we're getting for each weight. Divide weights by that so that even
the most sluggish weights get their chance to shine. 

3) Results achieved with AdamW = much faster convergence in 1/10th the number of cycles on some benchmark datasets.

4) Accuracy is as good as SGD + momentum, and almost always faster.

5) amsgrad - a paper claiming a problem with the convergence proof of Adam and fixed it. 
    amsgrad didn’t achieve any gain in accuracy (or other relevant metric) than plain Adam/AdamW

6) Adam generally requires more regularization than SGD, so be sure to adjust your regularization hyper-parameters when
 switching from SGD to Adam.
 
7) To use adamW in fast.ai, call like this - 
    a) learn.fit(lr, 1, wds=1e-4, use_wd_sched=True), ie use weight decay scheduled = True
    OR with new training API,
    b)  phases = [TrainingPhase(1, optim.Adam, lr, wds=1-e4, wd_loss=False)]
        learn.fit_opt_sched(phases)
            ie, wd_loss=False, for weight decay not computed in the loss

8) In the training loop, after computing the loss, subtract weight_decay * learning_rate from weight before the next 
step of the optimizer, as follows.

loss.backward()
for group in optimizer.param_groups():
    for param in group['params']:
        param.data = param.data.add(-wd * group['lr'], param.data)
optimizer.step()

9) With L2 regularization, best learning rate was 1e-6 with a max lr = 1e-3; 
   With weight_decay = 0.3, best lr = 3e-3

---------
https://arxiv.org/abs/1708.07120
Super-Convergence: Very Fast Training of Neural Networks Using Large Learning Rates
    Learning rate keeps growing for half the training.
---------
https://towardsdatascience.com/stochastic-gradient-descent-with-momentum-a84097641a5d

SGD with momentum key ideas 
1) Momentum is a smoothing function to reduce noisy data by taking an exponentially weighted moving avg of the gradients

2) Momentum has a hyperparam beta, we avg over 1 / (1 - beta) points of sequence for the moving avg.
    beta = 0.9 is a good value in practice.

3) Another perspective - Momentum uses previous gradients to influence movement of the optimizer to get over hills of 
    local minimums.    
********************************************************************************
LECTURE 13 - convolutions - deep dive 

    
By default, fastai puts data on the GPU when using data blocks.    
"""