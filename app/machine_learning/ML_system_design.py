"""
Machine learning system design from Chip Huyen, a Stanford instructor who teaches ML system design CS 329S
https://github.com/chiphuyen/machine-learning-systems-design/blob/master/build/build1/consolidated.pdf

Also reference:
https://github.com/alirezadir/machine-learning-interview-enlightener

https://developers.google.com/machine-learning/guides/rules-of-ml

Components -

1) Project setup

2) data pipeline
    a) Sampling
    b) randomization

------------

3) modeling & training
think of 3 different BASELINES -
    a) Random baseline - if model just predicts everything at random, whats the expected perf?
    b) human baseline - how well do humans perform on this task?
    c) simple heuristic - eg - recommending most popular app can have a  70% accuracy, does a sophisticated model do
        much better than this? It has to, to justify the cost

    DISTRIBUTED TRAINING
    Synchronous SGD where you wait for gradients to come from every machine before updating weights, slow machines
        can slow down the whole system.

    Async SGD - update weights as gradients come from each machine. Can lead to gradient staleness.

    MIXED PRECISION TRAINING
------------
    Model selection & benchmarking: autoML

------------
4) serving
    question your common assumptions
    a) prediction assumption
    b) IID
    c) smoothness
    d) tractability
    e) decision boundaries - linear vs non linear
    f) conditional independence

************************************************************

CASE STUDIES

A) AirBnB (2017) : predict value of homes
https://medium.com/airbnb-engineering/using-machine-learning-to-predict-value-of-homes-on-airbnb-9272d3d4739d

    1) MLAutomator: Automated tooling to convert jupyter notebooks to AirFlow pipelines

    2) Created Zipline - a feature repo that provides features at different levels of granularity such as guest, host,
        listing, market level
        2a) Zipline intelligently figures out join keys and backfills training datasets behind the scenes

    3) Use the pipeline(..) construct from scikit learn, solves a common problem of data transformation inconsistency
    when translating a prototype into production

    4) For insurance or credit screening apps, interpretability is the most important. Tree based models are not very
    interpretable. XGBoost significantly outperformed benchmark models such as mean response models, ridge regression
    models and single decision trees. This favors flexibility over interpretability.

    5) Notebook driven design reduces barrier to entry for data scientists

------------

B) Using ML to improve streaming quality @ Netflix (Mar 2018)
https://netflixtechblog.com/using-machine-learning-to-improve-streaming-quality-at-netflix-9651263ef09f

    a) adaptive buffering of 3 video qualities - HD, medium, and low quality , and switch based on bandwidth.

    b) intelligent prediction of what user will play next and caching it.
        eg - Next episode of a binge watched show is easy to predict based on contextual user history.
        Reduce time waiting for video to start when play is clicked.

    c) predict device failures reliably avoiding false positives. Statistical modeling to determine root cause while
        controlling for various covariates.

-------------

C) https://blog.acolyer.org/2019/10/07/150-successful-machine-learning-models/
6 lessons @ Booking.com (KDD Oct 2019)

    a) Randomized control trials to test business impact of your models - treatment group & control group like STRX
        learners for causal ML.

    b) uncanny valley effect: multi-hop destination recommender using markov chains. over-optimization of proxy metric
        like clicks fails to convert into desired business metric (closing a case due to finding a relevant article)

    c) Serving latency matters: 30% increase in latency cost us 0.5% in conversion rates. TODO - propose this DS
        experiment in EAR @ SFDC

    d) account for incomplete & delayed feedback

    e) For binary classification: Smooth bimodal distributions with one clear stable point are signs of a model that
    successfully distinguishes two classes. Response Distribution Analysis has proved to be a very useful tool that
    allows us to detect defects in the models very early.

-------------

D) https://medium.com/hackernoon/how-we-grew-from-0-to-4-million-women-on-our-fashion-app-with-a-vertical-machine-learning-approach-f8b7fc0a89d7
(2018)

-------------

E) https://medium.com/airbnb-engineering/machine-learning-powered-search-ranking-of-airbnb-experiences-110b4b1a0789
AirBnB experiences search & ranking problem

    STAGE 1: ML Baseline over rule-based model
    a) If booked, treat it as positive label, if clicked and not booked, treat it as negative.
    b) ranking model: gradient boosted decision tree model in v1 : task is binary classification with log-loss
        pro: no need to scale feature values or missing values.
        con: raw counts in fast growing marketplace can create instability in tree, better to use ratios or fractions
            eg - use booking to click ratio instead of raw booking counts
        offline evaluation: NDCG & AUC
    c) partial dependence plots of booking vs {price, ratings, view_count}

    d) ML ranking model improved bookings by 13% compared to rule based ranking model baseline. query params like
        # of guests , # of days etc were just filters for retrieval

    e) Offline ranking pipeline scheduled daily in AirFlow. Ordered list sent to production to show during search.

    STAGE 2 : Personalize
    a) Important to ensure no label leakage, ie only consider events at the time of click, before booking is made
        and not use info that happened after the booking is made.

    b) can only personalize for logged-in users but not for logged-out users

    c) increased bookings by +7.9% over stage 1

    d) look up table of userId to ranked list of personalized recommendations of experiences for that user. key 0 =
        ranking for logged out users

    e) Since O(NM) time complexity for personalized ranking of N users & M experiences, only limit to top 1M most active
        users.

    STAGE 3 : Online
    a) user-features: for 100s of Millions of users - kept in online key-value store and retrieved when user clicks on
        search box

    b) experience-features: 10s of Ks of experiences, kept in memory of search server

    c) query features: online

    d) moving to online KV store with RD/WR capabilities that can update user and experience features live as new
        reviews come into an experience or about a user.

    STAGE 4 : handle business rules such as promote quality

    a) discover potential new hits early using cold start signals

    b) enforcing diversity in top 8 results

    c) optimize search without location for clikcability eg - show top 18 experiences across locations, and then re-rank
        based on clicks

    MONITORING & EXPLAINABLE RANKING

    a) Helps to give hosts what factors lead to better rankings

    b) Dashboard to track ranking of specific experiences over time and the feature values for each ranked data point
        in time. TODO - can do this for EAR for top attached articles

    c) pair-wise loss is far more appropriate for ranking. ie booked vs clicked & not booked

    d) training labels - using different values for different user interactions is better . eg - 0.1 for click, 0.2 for
    click with selected date & time, 1.0 for booking, 1.2 for high quality booking. TODO for EAR.

-------------

F) https://eng.lyft.com/from-shallow-to-deep-learning-in-fraud-9dafcbcef743 (2018)

    a) Switched production algo from logistic regression to GBDT impl from XGBoost lib which gave 60% more precision
        for same recall and feature set.

    b) While GBDT was less interpretable, it learnt non-linear decision boundaries.
        Con: GBDTs do not gracefully handle sequential inputs like the histories of transactions, rides, and user
        activity

-------------

G) https://tech.instacart.com/space-time-and-groceries-a315925acf3a (2017)
Logistics @ Instacart (Jun 2017)

    a) jointly optimize expected time of delivery with speed of movement. This is vehicle routing problem with time
        windows.

    b) constraints: some have bigger cars, some have costco memberships where they can buy

    c) simple 1st cut Algo: sort orders by when they are due. Find person who can deliver that 1st order in time.
        Try to add orders s.t. it doesnt push 1st order beyond due time. dispatch th eorders. repeat.

    d) optimization problem: minimize Σ (idleness cost of shopper + lost effficiency cost + lost deliveries cost)

    e) location tracking: every 10s collect the latitutde, longitude, speed, direction of vehicle & accuracy reported by
    device.

    f) Datashader to visualize data points on map

    g) protect privacy of home delivery addresses by only showing store locations on map and location where drivers
        are moving quickly.

-------------

H) Scaling Michelangelo at Uber - structure of ML vs product teams
https://eng.uber.com/scaling-michelangelo/

-------------


"""