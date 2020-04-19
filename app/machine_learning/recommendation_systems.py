# -*- coding: utf-8 -*-
"""

Jan 20, 2020
realityengines.ai deep learning recommendation systems workshop - ZGC Innovation Center @ Silicon Valley
Non-temporal vs temporal ordering - search coffee makers on Tuesday vs a week from now. Seasonality patterns like
thanksgiving shopping. More important for Amazon.

Netflix - temporal data is less important.

Non-temporal data -
    for each user, split items 80/10/10 for train/ validation/ test

temporal -
    select points in time that give 80/10/10 split
    given a user and history, predict next item

Metrics -
top-n precision / recall -
    % of items from true top n in the predicted top n, for every user.
    % of items from predicted top n, in the true top n

top-n coverage - uniqueness of top-n items over the whole set

NDCG - gives higher weight to higher ranked items
-----------
Overview of Baselines -
1) Top popular
2) User/item k-nearest neighbors
3) Matrix factorization - to come up with good embeddings
U x d , d x V. Assume matrix has low dimension. Find the best "latent factors"
----
Automated featurization.
GRU for temporal data.
Input dimensions? Length of the item attribute, 1 more dimension for time.

Links to notebook -
bit.ly/realityengines
bit.ly/customRecommendations

---
Amazon doesnt use Deep Learning.

Some popular recommender systems NN architecture papers -
1) youtube recommender system
2) pixie pinterest recommender system
3) latent cross RNN
4) google play

********************************************************************************
TODO - read
https://medium.com/recombee-blog/machine-learning-for-recommender-systems-part-1-algorithms-evaluation-and-cold-start-6f696683d0ed
http://www.quuxlabs.com/blog/2010/09/matrix-factorization-a-simple-tutorial-and-implementation-in-python/, 
https://datasciencemadesimpler.wordpress.com/tag/alternating-least-squares/, 

***** reco sys book reading notes ******

PCA (principal components analysis) assumes the original data is gaussian distributed. If this assumption is wrong, there is no
guarantee that using it will reduce dimensionality.
In such cases, SVD and non-negative matrix factorization (MF) are more effective. SVD is the basis
for LSA

item concept * concept strength * concept features


MF is better than SVD in handling missing values by adding a bias term.

---------
k nearest neighbours (kNN) is a lazy learner since it does not build models explicitly, but just
computes the k-nearest neighbours of a query point and takes the majority label to assign to the
query point. But how to decide k is the big question. Its 1 of the simplest ML classification
algorithms.

-------
gini index is a measure of impurity in a decision tree.
-------------
bayesian classifiers using conditional probability are useful during cold-start conditions.

**** end reco sys book reading notes *******
------------------

***** ------------------    Notes from Leah McGuire talk (SFDC PMTS Einstein)  *************
https://www.youtube.com/watch?time_continue=570&v=Eh802ZeAcC4

1) item-item similarity (jaccard similarity  = (A intersect B) / (A U B)) recommenders are more stable and scalable
    than user-item similarity.

2) Matrix factorization methods and item-item similarity approaches work better than restricted boltzmann machines.
    User-Product matrix = N x M matrix
    Can be represented in reduced dimensionality as as Users N x K matrix   matrix-multiply Products K x M matrix
    Parallelizable with Alternating Least Squares (ALS). Can be applied to implicit data (impl is in MLLib)

    Difference between implicit vs explicit matrix factorization -
    min(x,y) Σ_(u,i) (c_ui(p_ui - x_uT yi)^2 + λ(Σ||x_u||^2 + Σ||y_i||^2)

    c_ui = 1+ αr_ui where c = confidence you have that the person liked a product
    Ρ_ui = 1 if r_ui > 0 ; 0 if r_ui = 0 where r = rating or number of times the person purchased the product
    P = preference of user for a product

    λ = penalty on terms you compute, to prevent over-fitting.
    α = hyper-parameter in the confidence that you tune

Issues in training & evaluation:
    0) Training data consists only of purchases (+ve examples). Is missing data negative or just missing?

        a) Generate -ve values for evaluation.
        Chances are random unrated data assigned as -ve will not be good examples.

        b) Focus on top-K predictions and see if hold-out appears in recommendations.

    1) Choose the evaluation metric that best matches what you are trying to do:
        a) are results presented as a short vs long list?
        b) are you predicting a rating?

    2) Be aware of biases in offline evaluation
        a) top-K can bias towards popular items => less personalization
        b) ROC, precision, recall do not tell you anything about how good the ordering is

    3) Models have lots of levers to tweak

------------------------------
What not to use in model selection - Root mean square error. Its not a helpful measure.
Its not appropriate for unary data (with only +ve labels). Highly dependent on how many negative examples you generate.
Not useful for predicting performance across models. Misleading for hyper-parameter selection.

For top-K, recall can be a good measure. Top-K can be computationally expensive to generate.

-------------
Rank metrics for top-K

1) Discounted cumulative gain (DCG) can be hard for personal recommendations without a true ranking measure.
2) Mean reciprocal rank is more forgiving.
    If presenting data in a long list, MRR is a better metric than recall.

Query | Results              | Correct response | Rank | Reciprocal Rank
cat   | catten, cati, cats   | cats             | 3    | 1/3
torus | torii, tori, toruses | tori             | 2    | 1/2
virus | viruses, virii, viri | viruses          | 1    | 1

MRR = 1/|Q| Σ(i = 1 to |Q|) 1/rank_i

Intuition: Results appearing lower in search results are penalized.
-----------
Application (ie use case) dictates how often the model must be updated. Item Nearest Neighbors and Matrix factorization
can be used with data updated since training. Decrease the need for refitting model.
--------------
Combining information to build new models for better results (eg - User geolocation & IP address info)
Item popularity - popular items are often relevant.

"Learning to rank" - The way you incorporate the above information into an existing model without these features
 about popularity, geolocation, IP-address etc is called learning to rank.
If you have recommendation_score & item_popularity_score, have weights for both of these scores.
Combine them to produce a new score thru learning-to-rank.
-----------
1) For cold start problem, having the right defaults can help a lot. Eg - when there are lots of new users,
serving up the most popular items can give a huge lift (> 20% lift in recall on some data sets).



***** ------------------    Notes from Leah McGuire talk (SFDC PMTS Einstein)  *************

"""
