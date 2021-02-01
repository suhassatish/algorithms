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
    e) hover action on live-site (if available - instrument this. This is already proposed by Kukesh)
    f) visual similarity / item similarity metrics
    g) per user, similarity of past similar-product recommendations
    h) frequency of email campaigns
    i) weights for order > add to cart action > click action
    j) clicks / session-length

Recall @ k, hit rate @ 1, normalized discounted cumulative gain (NDCG), mean reciprocal rank (MRR),
mean avg precision (MAP)

************************************************************************

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


************************************************************************
For similar products, use a computer-vision based recommender from mmfashion
https://github.com/open-mmlab/mmfashion

https://github.com/open-mmlab/mmfashion/blob/master/mmfashion/models/fashion_recommender/type_aware_recommend.py


************************************************************************

4) explore public datasets
5) openCV MMFashion lib - find product compatibility
    a) Based on this paper for polyvore dataset - https://arxiv.org/pdf/1803.09196.pdf
        Learning Type-Aware Embeddings for Fashion Compatibility - Jul 27, 2018
    Notes from paper -
    1) 1st learn single shared embedding space. Then project from it to subspaces identified by type. Eg - all shoes
        that match a given top MUST be close in shoe-top space but can be very different in the general embedding space.

    2) Do not respect types, ie a shoes embed into same spaces that hats do. This means a shoe should match a blouse
        and a hat should match a blouse, but the hat may not actually match the blouse in reality. In other words,
        items should be allowed to match in 1 context and not match in another. Thus, an embedding that clusters items
        close together is not a natural way to measure compatibility without paying attention to context.

    3) By learning type-respecting spaces to measure compatibility, we avoid the issues stemming from using a single
    embedding.

    4) General emb trained using Visual semantic loss b/w image emb and features representing a text description of item

    5) we use a learned projection which maps our general embedding to a secondary embedding space that scores
        compatibility between two item types.

    6) Metric = triplet loss
    In the triplet loss, rather than minimizing Euclidean distance between compatible items and maximizing the same for
    incompatible ones, an empirically more robust way is to optimize over the inner products instead.
    To generalize the distance metric, we take an element-wise product of the embedding vectors in the type-specific
    spaces and feed it into a fully-connected layer, the learned weights of which act as a generalized distance function

    7) Ablation study
    we see that using a FC layer provides a small performance improvement at a higher computation cost while our learned
    metric performs slightly better than using cosine distance.


-----------------
    b) https://arxiv.org/pdf/1707.05691.pdf
        Learning Fashion Compatibility with Bidirectional LSTMs - Jul 2017

************************************************************************

7) sequential: build a model to recommend user's next best action based on their browsing history

priority: metrics > hybrid > sequential (after 1-month) (has to understand the dimension of time)

hybrid approach == pass in userId and product interaction, can pass in side-features optionally.
************************************************************************

8) Microsoft research has code for various types of recommender systems - Explore it
    https://github.com/microsoft/recommenders

********************************************************************************
Mon, Jan 18, 2021 - standup
Choi
demo/test_fashion_recommender.py

compatibility == shirt matches with shorts or not

Snapshot of dataset, 50K interaction. 1 side product details, color , fit. Other side - user side featuer, opens email
frequently, etc.

Model learns embeddings. Hybrid approach => passing in hard features now.  Extract embedding features from MMfashion.
price level, fit level and fashion taste.
-----

Tracking impressions.
clicked, add to cart or purchased.


dockers.com/US/en_US

cold start problem = generic recommendations based on geography, device. This comes up on home page.

Not able to deploy live model due to latency issues, cost-to-serve model. Website-level rec and email-level rec.

Everything goes live 1st in email campaigns. Optimize customer's preference.

purchase rank =5, add_to_cart = 4, click = 3, view = 2
apv = preference_product_value

item_data is where we'll make the interaction effects.

Metrics - give a proposal. Ways to evaluate the model. Metrics would capture model performance in various ways.

Combine to single optimization metric for optimizer.

---

1) how to extract hybrid embeddings
2) understand how MMFashion works
3) how to integrate it with turi create

using MF machines, there are tons of model based approaches. Finally we can compare.


********************************************************************************
Wed Jan 20,2021 - scrum discussion

rank for each interaction - model was able to differentiate at the expense of quality of recommendation.

model initially picked up shade, etc.

keep -ve sampling constant.

preserve ranking model. give higher importance to conversion products.

impute values for aov and apv.
cap to most recent 20 interactions.

have data for 200K users and 2.4M products.
Match session_id, if opted-in for email campaign, match email_id with session_id. thats how sale affinity is measured.

maximize margin for ppl with high sale_affinity who buy even without any discount. Sale_affinity inferred from email
engagement.

objective function - what to optimize?

20-40% customers lost due to no 1:1 mapping b/w website interaction and email.
out of 1.1M, 280k-300k have geo location data.

age group category data?

any luck on combining embeddings for mmfashion?
combines textual embeddings with image embeddings - launchpad website.

mmfashion gives COMPATIBILITY SCORE for complementary products - item - item similarity.
not using recommender from mmfashion. just use the learnt embeddings from mmfashion. then pass that into turicreate.

if we pass in embeddings as side feature into .

do you have complimentary fashion products labeled dataset?
---

embeddings.py - can strip head of pretrained model and use embeddings directly, no need to use .

cart page and product page recommendation - diversity matters.
home page - similar products, no diversity.


"""