"""
https://arxiv.org/pdf/2008.12134v1.pdf
Paper reading fellowship.ai session on  Jan 13, 2020 (presenter: Rahat Santosh)
Siamese N/W for RGD-D Salient Object Detection - 26 Aug, 2020 - Keren Fu et al
Application of Siamese N/W = signature comparison

1) Traditionally, RGD and depth are treated as independent info and separate N/Ws designed for feature eng from each.

2) JL-DCF ie joint-learning desnsely cooperative fusion arch is designed to learn from RGD and depth i/ps thru a
shared N/W backbone called Siamese arch.

3) Paper advances state-of-the-art by ~2% F-measure across 7 challenging datasets.

S-measure of accuracy = spatial structure similarity of binarized outputs of 2 images
S_r = region-aware structural similarity
S_f = final saliency model

E-measure = enhanced measure for combining 2 binary maps.

If depth data is missing in most datasets, we can use the below -
There are some monocular depth estimation tasks. Depth map estimation using open-CV, they're not very accurate.
Not sure how people come up with ground truth.
------------------------------------------------------------------------------------------------

Zero-shot learning is a method in which at test time, a few new classes are introduced that were never seen in training
data. The model has to predict the category they belong to.


"""