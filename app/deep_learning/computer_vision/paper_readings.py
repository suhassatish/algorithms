"""
https://arxiv.org/pdf/2008.12134v1.pdf
Paper reading fellowship.ai session on  Jan 13, 2020
Siamese N/W for RGD-D Salient Object Detection - 26 Aug, 2020 - Keren Fu et al

1) Traditionally, RGD and depth are treated as independent info and separate N/Ws designed for feature eng from each.

2) JL-DCF ie joint-learning desnsely cooperative fusion arch is designed to learn from RGD and depth i/ps thru a
shared N/W backbone called Siamese arch.

3) Paper advances state-of-the-art by ~2% F-measure across 7 challenging datasets.

------------------------------------------------------------------------------------------------

Zero-shot learning is a method in which at test time, a few new classes are introduced that were never seen in training
data. The model has to predict the category they belong to.


"""