# -*- coding: utf-8 -*-
"""
************************************************************************
FACTORIZATION MACHINES (FM) - https://www.csie.ntu.edu.tw/~b97053/paper/Rendle2010FM.pdf
1) A FM is a general predictor that combines advantages of SVMs with factorization models.

2) Unlike SVMs, they model all INTERACTIONS (eg user item interactions in rec sys) b/w variables using factorized params

3) Hence, they can estimate interactions even where there's huge sparsity (eg rec sys) where SVMs fail.

4) Model equations in FMs can be calculated in linear time and hence, FMs can be optimized directly.

5) Traditional matrix factorization methods like SVD++, PITF (pairwise interaction tensor factorization)
    or FPMC (factorized personalized markov chains) fail for COLD-START situations when there is no
    user interaction data for items. They're also not applicable for general prediction tasks since their model eqns
    and optz algos are derived individually for each task. FMs can mimic these models by specifying input data (
    ie feature vectors). THis makes FMs easily applicable even for users w/o expert knowledge of factorization models.

6) To learn the FM model, we typically use
    a) MSE loss for regression task,
    b) cross entropy loss for classification tasks, and
    c) BPR loss for ranking task.
    Standard optimizers such as SGD and Adam are viable for optimization.

7) it’s not immediately obvious how to adapt FM models for implicit feedback data. One naïve approach would be to label
 all observed user-item interactions as (1) and all unobserved interactions as (-1) and train the model using a common
 classification loss function such as hinge or log loss. But with real-world recommendation data sets this would require
  the creation of billions of unobserved user-item training samples and result in a severe class imbalance due to
  interaction sparsity. This approach also has the same conceptual problem as the implicit feedback MF adaptation:
  it’s still minimizing RATING PREDICTION ERROR instead of directly optimizing ITEM RANK-ORDER.
    Source - https://towardsdatascience.com/factorization-machines-for-item-recommendation-with-implicit-feedback-data-5655a7c749db

8) https://github.com/etlundquist/rankfm
RankFM: a new python package for building and evaluating FM models for recommendation problems with implicit feedback
data
************************************************************************

paper - https://arxiv.org/pdf/1905.01997.pdf
Deep Learning sequential recommendation: algorithms, influential factors and evaluations
Oct 10, 2020

For sequential rec sys, DL-based methods have recently surpassed traditional models like matrix-factorization (MF) based
ones and markov-chain (MC) based models.

PROS of DL -
1) MC and MF methods assume a user's BH is only related to a few recent actions but DL methods can have a much longer
    sequence.
2) DL methods are more robust to sparse data and can adapt to varied length of i/p seq.
CONS of DL -
1) lack of interpretability
2) optz is v/difficult and needs more training data
3) They largely emphasize item representation, but lack of a careful design on user representation.

Important to model user's short term interests within a session as well as their long term interests across sessions.
Markov-chain and sesion-based KNN have traditionally been used to model these effects before DL-based RNNs.

Behavior trajectory is a sequence of (behaviour actions on behavior object) tuples.
1) experience-based - interact with same object in different way, eg - search, click, buy
2) transaction-based - different objects but same behavior, eg - buy item 1, buy item 2 , etc
3) interaction-based - hybrid of above 2. Predict the next BH obj user will interact with.
------
TRADITIONAL APPROACHES -
1) FREQUENT PATTERN MINING with sufficient support and confidence.
    Recommend frequently co-occuring items
    PROS -
        1) Easy to interpret
    CONS -
        1) Scalability issue for large number of items, it becomes too restrictive
        2) Choosing threshold for min support and confidence is tricky. Too low and random things recommended, too high
            a threshold and you will only recommend very sparsely to really similar users.

2) K-NEAREST NEIGHBORS - 2 types -
    a) item-based KNN - Considers last BH in a given session and similar items in current session based on
        cosine-similarity.
    b) session-based KNN - Compares current session with all previous sessions and similarity based on jaccard or cosine
        on binary vectors in item space.

    PROS -
        a) highly explainable
    CONS -
        a) Sequential dependency among items not captured.

3) MARKOV CHAINS (MC) - 1st order MC only considers the most recent BH. Higher order MCs are required for long sequences
    PROS - sequences captured
    CONS -
        a) Fails to capture more intricate dynamics of complex scenarios.
        b) data sparsity issues

4) MF - BPR-MF optimizes pair-wise user-item ranking objective function with SGD.
    CONS - a) only low-order effects among latent factors are considered.
        b) except a handful of algos like timeSVD++, others ignore time effects both within and across sessions.

5) REINFORCEMENT LEARNING - This learns from user actions dynamically.

6) RNNs
    a) GRU4Rec proposed popular item sampling and uniform sampling that significantly improved perf.

    b) Context-aware RNN ie CA-RNN considers user's context such as location, time of day, age, etc

    c) With self-attention, it is capable of estimating weights of each item in the user’s interaction trajectories
    to learn more accurate representations of the user’s short-term intention, while it uses a metric
    learning framework to learn the user’s long-term interest.

    Side info such as item ID, first level category, leaf category, brand and shop in the user’s historical transactions

   CONS -
   a) Dont support parallelisem that well.
   b) Can only model 1-way transitions b/w consecutive items

7) A paper explored variational autoencoder for modeling a user’s preference through his/her historical sequence, which
combines latent variables with temporal dependencies for preference modeling.

Metrics - Besides accuracy, DIVERSITY of recommendations is also an important business metric to measure.

************************************************************************

Apr 10, 2020 - Real-time, Contextual and Personalized Recommendations
https://www.youtube.com/watch?v=2qood2d-HYk

COLLABORATIVE FILTERING - has 2 types
    a) MEMORY BASED APPROACH - Find similar users based on cosine similarity or pearson correlation & take weighted avg
        of ratings.
        Pro: Easy creation and explainability of results
        Con: Poor performance for sparse data, so non scalable
    b) MODEL BASED APPROACH - use ML to find user ratings of unrated items. eg - PCA, SVD, NN, Matrix factorization.
        Pro: Dimensionality reduction deals with missing or sparse data
        Con: Inference is intractable due to hidden / latent factors.

Big drawback - cold-start problem for new product launches.

CONTENT BASED FILTERING MODEL - used for cold-start.
    a) Purchase behavior
    b) Text embeddings - word2vec, TFIDF, etc for document similarity
    c) Image embeddings - transfer learning with DeepImageFeaturizer, ResNet model architecture with softmax activation
        at the end, etc. Can use this model & add dense layers and dropout and take embeddings from penultimate layer of
        transfer learned model.

HOW TO PERSONALIZE?
    a) Awareness - 1st time visitors, start of shopping journey
        Candidate generation: - popularity based recommendation to get top 40 products
        Success Metrics: AUR (avg unit retail ie avg $ amt spent for particular type of item),
            UPT (units (purchased) per TX), CTR, etc
        Ranking: location closer to user / device / seasonal purchase patterns

    b) Consideration - browsing history, early exploration phase. Visitors with past 1 month / in-session browsing BH
        Candidate generation: product attr & product interaction
        Ranking: Based on last product interacted weighted by intent (click, add to cart, etc)

    c) Purchase - strong positive. Visitors who have purchased in last 6 months.
        Candidate generation:
            1) Rank browsing interactions after purchase with intent and time to find top 10 products that will be
                liked by user.
            2) Collaborative filtering to find similar users and auxillary accessory items
        Ranking: based on intent and actions

ENGINEERING ARCHITECTURE v1 - Used elastic search, but it dodnt work well for them.

ENGINEERING ARCHITECTURE v3 - Ref: ~/Dropbox/Tech_extras/recommender_systems/arch-v3Apr2020-ecommerce.png
    Click stream data -> segment web hook -> publish to SNS MQ -> subscribed by AWS lambda to filter -> WR to redis.

    Client User Request -> (product code) -> Api Gateway -> Trigger AWS Lambda indexer -> DynamoDB WR ->
        Triggers AWS Lambda parser to query Redis
    Web Server Response Path:
        Redis returns query result -> AWS lambda ranks the returned result set -> WR ranked results to dynamoDB ->
            Triggers AWS Lambda to call API gateway with response -> Similar products shown to client user

    Hybris -> replicate to Redshift -> Transactions purchases / returns -> Matri factorization stored in EC2 -> WR to
        redis

ENGG ARCH v4:
    AWS ELB Elastic Load Balancers

ENGG ARCH v5:
    Adds ECS EC2 Container Service
    ECR - Elastic Container Registry
    AWS Batch
    Batch Jobs Scheduling AWS Step Functions (helps stitch apps using Lambda, Fargate & Sagemaker)
    Kinesis for user segments filtering and ingestion

PERSONALIZATION THINKING AHEAD -
    1) Ask users' permissions to take their instagram fashion style photos (eg Levi's jeans) to personalize recs.
    2) ranking algorithms
    3) Purchase propensity based recommendations
    4) Customer lifetime value based recommendations

Q&A:
    Q: How are you solving for position bias?
    A: Noticing people clicking on 10th rec. Learning to rank algorithm will solve for this.

    Q: Biggest challenge?
    A: Business buy-in & getting stakeholder trust. Start simple with easily interpretable models.

    Q: Which worked well?
    A: item-based filtering worked better. Because everyone bought men's jeans.

********************************************************************************
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

NDCG - gives higher weight to higher ranked items that are clicked and vice versa.
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

Some popular recommender systems NN architecture papers - TODO
1) youtube recommender system
2) pixie pinterest recommender system
3) latent cross RNN
4) google play

********************************************************************************
TODO - read
https://medium.com/recombee-blog/machine-learning-for-recommender-systems-part-1-algorithms-evaluation-and-cold-start-6f696683d0ed
https://datasciencemadesimpler.wordpress.com/tag/alternating-least-squares/, (ALS)

***** reco sys book reading notes ***************************************************

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
algorithms. It is computationally intensive at inference time.

-------
gini index is a measure of impurity in a decision tree.
-------------
bayesian classifiers using conditional probability are useful during cold-start conditions.

**** end reco sys book reading notes ****************************************************
------------------

**************************************************    Notes from Leah McGuire talk (SFDC PMTS Einstein)  *************
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

LEARNING TO RANK (LTR) - Its an optz technique that learns rank-order directly instead of minimizing prediction error.
If you have recommendation_score & item_popularity_score, have weights for both of these scores.
Combine them to produce a new score thru learning-to-rank.

LTR models train on pairs or lists of training samples instead of individual observations. The loss functions are based
on the relative ordering of items instead of their raw scores. Models using LTR have produced state-of-the-art results
in search, information retrieval, and collaborative filtering. These techniques are the key to adapting FM models to
implicit feedback recommendation problems.
One of the most popular LTR techniques for item recommendation is Bayesian Personalized Ranking (BPR). BPR attempts to
learn the correct rank-ordering of items for each user by maximizing the posterior probability (MAP) of the model
parameters given a data set of observed user-item preferences and a chosen prior distribution. Each user’s observed
items (implicit feedback) are assumed to be preferred over the unobserved items, and all pairwise preferences are
assumed to be independent. To learn these preferences, one creates training samples comprised of [user (u), observed
item (i), unobserved item (j)] tuples and maximizes the following log-likelihood function with respect to the model
parameters.

Max_θ ln[p(>_u | θ) p(θ)]
where (>_u | θ) is the model's predicted item ranking for user u.

Source: https://towardsdatascience.com/factorization-machines-for-item-recommendation-with-implicit-feedback-data-5655a7c749db
-----------
WEIGHTED APPROXIMATE PAIRWISE RANK (WARP) doesn’t simply sample unobserved items (j) at random, but rather samples many
unobserved items for each observed training sample until it finds a rank-reversal for the user, thus yielding a more
informative gradient update. This is especially important in contexts with a large number of items and highly skewed
item popularity (very common).

The basic procedure is:
1. Randomly sample an unobserved item for the user and compute its utility score. If the unobserved item’s score exceeds
 the observed item’s score plus a fixed margin then make a gradient update, otherwise continue to sample negative items
2. Scale the magnitude of the gradient update based on the number of negative items sampled before finding a margin
violation — make smaller updates if more negative items were sampled as it’s more likely the model is currently ranking
 user preferences correctly

In fact, if you scale the magnitude of the gradient updates with a (0, 1] multiplier, BPR can be seen as a special case
of WARP where the maximum number of negative samples is equal to one, resulting in a constant gradient update multiplier
 of one. Using WARP increases per-epoch training time relative to BPR, but often yields faster convergence and superior
 model performance.

Source: https://towardsdatascience.com/factorization-machines-for-item-recommendation-with-implicit-feedback-data-5655a7c749db

Above link also shows that FM model incorporating auxiliary features and trained using LTR optimization techniques
yields superior performance relative to a similarly-specified classical MF model with ALS.

------------
1) For cold start problem, having the right defaults can help a lot. Eg - when there are lots of new users,
serving up the most popular items can give a huge lift (> 20% lift in recall on some data sets).

**************************************************   Notes from Leah McGuire talk (SFDC PMTS Einstein)  *************

"""
