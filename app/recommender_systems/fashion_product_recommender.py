"""
https://fellowshipai.wordpress.com/2021/01/11/project-product-recommender/

Fri, Jan 15, 2021
Email recommendation system

1) Metrics
Recs in 2 channels - live site and email campaigns. Capture quality metrics in both channels.

    a) Clicks / (emails sent)
    b) index of item that clicked
    c) avg order value
    d) conversion rate = (# of purchases in session) / (# of clicks in session)
    e) hover action on live-site (if available - instrument this. TODO)
    f) visual similarity / item similarity metrics
    g) per user, similarity of past similar-product recommendations
    h) frequency of email campaigns
    i) weights for order > add to cart action > click action
    j) clicks / session-length
-----
2) Turicreate
3) currently model-based recommender that uses product-level and user-level features, explore factorization based.
https://apple.github.io/turicreate/docs/api/generated/turicreate.recommender.ranking_factorization_recommender.RankingFactorizationRecommender.html

Ranking Factorization Recommender -
Learns user & item latent factors and ranks them on likelihood of observing those (user, item) pairs. Useful for
collaborative filtering with implicit feedback datasets or with explicit ratings where ranking is desired.

while Matrix Factorization learns latent factors for only the user and item interactions, the Factorization Machine
learns latent factors for all variables, including side features, and also allows for interactions between all pairs of
variables.

using linear_side_features=True performs better in terms of RMSE, but may require a longer training time.
υ (upsilon)


--------------------
For similar products, use a computer-vision based recommender from mmfashion
https://github.com/open-mmlab/mmfashion

https://github.com/open-mmlab/mmfashion/blob/master/mmfashion/models/fashion_recommender/type_aware_recommend.py


------------------
paper - https://arxiv.org/pdf/1905.01997.pdf
Deep Learning sequential recommendation: algorithms, influential factors and evaluations
Oct 10, 2020

For sequential rec sys, DL-based methods have recently surpassed traditional models like matrix-factorization (MF) based
ones and markov-chain (MC) based models.

1) MC and MF methods assume a user's BH is only related to a few recent actions but DL methods can have a much longer
    sequence.
2) DL methods are more robust to sparse data and can adapt to varied length of i/p seq.
Cons of DL -
1) lack of interpretability
2) optz is v/difficult and needs more training data

------------------
4) explore public datasets
5) openCV MMFashion lib - find product compatibility




7) build a model to recommend user's next best action based on their browsing history

priority: metrics > hybrid > sequential (after 1-month)
********************************************************************************


"""