"""
https://www.youtube.com/watch?v=dafU1SZs4iw
Talk on Jan 7, 2021 - distributed ML to learn causal inference effect using fugue and spark

Business Example - give 50% coupon to lyft frequent customers but only 20% coupon to infrequent customers
How do you measure outcomes when you have limited marketing budgets on whom to target for which coupons?

Solution - Co-variate matching. Match users based on similar co-variates. Then make in-group comparisons.
When the co-variates have high dimension (eg - location, time of day of ride, etc), matching doesnt work. We need models

T-learner ie two-learner - takes 2 estimators - take difference of 2 estimators where we condition on treated,
    condition on controlled and from those co-variates, build a model that takes the difference.

Issues with T-learner example -
1) Need a different model for each coupon
2) Large number of model types -
model       | description                           | use case
t-learner | difference of 2 estimators on treated / control  | simple to no confounding
x-learner | uses t-learner o/p to regress on difference b/ treatment / control | num treated << num control
r-learner | uses robinson Tx to derive explicit loss under strong assumptions | general but quite unstable
s-learner | treats treatment variable as same as all other covariates | when there is 0 treatment effect
causal forest | maximizes diff in treatment effect due to covariates in leafs | for interpretability, but packages dont
    scale well

all of these have different loss functions.

3) Dont have access to counterfactuals, so how to validate models?

************************************************************************************************************************

Demystifying uplift models for targeted marketing strategy optimization
https://medium.com/datadriveninvestor/simple-machine-learning-techniques-to-improve-your-marketing-strategy-demystifying-uplift-models-dc4fb3f927a2

uplift/incremental/true lift/net modelling directly models the incremental impact of a treatment (such as directed
marketing action) on an individual's behavior.

Avoids "sleeping dogs" ie those who buy your products but stop doing so if they're included in marketing campaigns.
Eg - mistargeted maternity wear ad to someone thats not expecting may lead to privacy concerns.

----------------

Test data evaluation metrics -

1) Incremental Response Rate (IRR) =
(purchases in treatment grp) / (# customers in treatment grp) - (purchases in ctrl group) / (# customers in ctrl group)

2) Net Incremental Revenue (NIR) = 10 * purchase_treatment - 0.15 * customers_treatment - 10 * purchase_ctrl

Other related metrics: https://github.com/uber/causalml
3) Conditional Avg Treatment Effect (CATE)
    identifies the target customers by estimating the effect of the KPI from ad exposure at the individual level from
    A/B experiment or historical observational data

4) Individual Treatment Effect (ITE)
    A company has multiple options to interact with its customers such as different product choices in up-sell or
    messaging channels for communications. One can use CATE to estimate the heterogeneous treatment effect for each
    customer and treatment option combination for an optimal personalized recommendation system.

From :  https://pbiecek.github.io/xai_stories/story-uplift-marketing1.html,
5)   QINI CURVE is not suggested for performance evaluation of uplift models as it is vulnerable to overfitting to
    the treatment label. Therefore, the CUMULATIVE GAIN chart is used. It is the least biased estimate of the uplift.

6) Interpretability per customer: SHAP (SHapley Additive exPlanations)
Because of additive property of SHAP, if we use any tree-based model, we can make use of tree-based kernel for SHAP
value estimation (faster and better  convergent) instead of modeling it directly as a black-box (uplift) model.

For getting SHAP values from uplift model ,KernelExplainer was used to sample records (due to algo's time complexity).
This introduced some randomness in the results.

----------------
Model Approach 1:

Label 1 to ppl who received promo & converted, 0 otherwise.

Balance classes 1:1 by upsampling minority class and feed into
model = xgb.XGBClassifier(learning_rate = 0.1,\
                          max_depth = 7,\
                          min_child_weight = 5,\
                          objective = 'binary:logistic',\
                          seed = 42,\
                          gamma = 0.1,\
                          silent = True)

If model predicts 1, that person should be sent an ad campaign, otherwise none.

----------------

Model Approach 2:
Train 2 models, 1 on treatment group & 1 on control group.
M1 predicts P(respond | treatment)
M2 predicts P(respond | no treatment)

Lift = P(purchase | treatment) - P(purchase | control)
Send promos only to top5  %ile lift candidates.

Result: This model results were less spectacular than approach 1.
Disadvantage:
1) The difference in probabilities may not model the lift correctly.
2) Errors could be doubled since both models contribute errors.
3) Model scales could be different.

----------------

Model Approach 3: Using a Single Model with Treatment Indicator Variable

1) Train a single model on both treatment and control group w/ an indicator variable tracking which groups ppl belong to
2) For a new individual, use the trained model with indicator variable set to 1 to predict P(response | treatment = 1)
3) use the trained model with indicator variable set to 0 to predict P(response | treatment = 0)
4) 2) - 3) will tell how new inidividual will respond to your marketing campaign
"""
from xgboost import XGBClassifier
test = []
model = XGBClassifier(learning_rate=0.1,
                      max_depth=7,
                      min_child_weight=5,
                      objective='binary:logistic',
                      seed=42,
                      gamma=0.1,
                      silent=True)

# compared to the above hyperparams, https://pbiecek.github.io/xai_stories/story-uplift-marketing1.html has
# the following major hyper params : maximum depth of 5, high learning rate of 0.7 and only 12 estimators

# To predict whether a new individual should receive a promotion
# Fit a model with treatment = 1 for all data points
test['treatment'] = 1.0
preds_treat = model.predict_proba(test, \
                                  ntree_limit=model.best_ntree_limit)

# Fit a model with treatment = 0 for all data points
test['treatment'] = 0.0
preds_cont = model.predict_proba(test, ntree_limit=model.best_ntree_limit)

lift = preds_treat[:, 1] - preds_cont[:, 1]

# ----------------------------------------------------------------------------------------------------------------

"""
Model Approach 4: Multi-class classification with 4 classes below

1) TR: the treatment and response group. Individuals in this group received a treatment (promotion) and responded 
(made a purchase)
2) CR: the control and response group. Individuals in this group received no treatment (no promotion) but still 
responded (made a purchase)
3) TN: the treatment and no response group. Individuals in this group received a treatment (promotion) but did not 
respond (made no purchase)
4) CN: the control and no response group. Individuals in this group received no treatment (no promotion) and did not 
respond (made no purchase)
"""
train_data = []
target = []
for index, row in train_data.iterrows():
    if (row['Promotion'] == "Yes") & (row['purchase'] == 1):
        # TR group
        target.append(0)
    elif (row['Promotion'] == "No") & (row['purchase'] == 1):
        # CR group
        target.append(1)
    elif (row['Promotion'] == "Yes") & (row['purchase'] == 0):
        # TN group
        target.append(2)
    else: #CN group
        target.append(3)
train_data['target'] = target

# https://github.com/joshxinjie/Data_Scientist_Nanodegree/tree/master/starbucks_portfolio_exercise

# **********************************************************************************************************************
"""
Conclusions from  - https://pbiecek.github.io/xai_stories/story-uplift-marketing1.html
1) Regardless of the customer groups (persuadables, sleeping dogs, lost causes, sure things), always history and womens 
are among three most important features.

2) For observations with considerable negative uplift (‘sleeping dogs’) both history and womens have negative 
correlation with their SHAP values. 

3) In the case of ‘sure things and lost causes’, womens has positive correlation whereas history has negative. 

4) The same variables among ‘persuadables’ (considerable positive uplift) have positive correlation with SHAP values. 

5) Correlation changes gradually with uplift value. What is interesting is the fact that regarding zip code only the 
information whether someone is from rural area is important. Note that this category of dwelling place was the least 
popular among customers. 

6) Information about purchase channel in general has relatively small predictive power.

7) If a person is a newbie, it is harder to encourage him/her to buy a product through marketing campaign

8) most important thing to check is whether the model is overfitted. The tool that can help in verifying model 
sensitivity is the Partial Dependence Plot. In the case of our model it can be seen that the model is slightly 
overfitted as there is a peak on PDP of history.

9) Sweet spot to send email is 2 months after purchase.

10) In the case when someone buys from men’s and women’s collections we should send e-mails dedicated to women.

# **********************************************************************************************************************
Capabilities of Uber causal-ml repo - https://github.com/uber/causalml
~/Dropbox/tech_extras/ML/causalML/


"""
