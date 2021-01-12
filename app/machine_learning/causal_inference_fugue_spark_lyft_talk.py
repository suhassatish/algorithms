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



"""