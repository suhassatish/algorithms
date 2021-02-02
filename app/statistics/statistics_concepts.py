# -*- coding: utf-8 -*-
"""
t-statistic - Number of standard deviations a param is away from a constant.

--------------------------------------
R-squared - Explains how much variance in the model can be explained by a certain feature or features.

--------------------------------------
Heteroskedasticity - A vector of random variables is heteroskedastic if the variance of random disturbances is different
across elements of the vector.
The existence of heteroscedasticity is a major concern in regression analysis and the analysis of variance, as it
invalidates statistical tests of significance that assume that the modelling errors all have the same variance.

While the ordinary least squares estimator is still unbiased in the presence of heteroscedasticity, it is inefficient
and generalized least squares should be used instead.

--------------------------------------
NULL HYPOTHESIS is usually a statement, which the scientists want to prove wrong. But will start assuming its true.

--------------------------------------
F-statistic

F = [(TSS - RSS) / p ] / [ RSS / (n - p - 1)]
TSS = total sum of squares
RSS = residual sum of squares
n = number of samples
p = number of features

Used by the F-test to test if groups of features are jointly statistically significant.


--------------------------------------
PEARSON CORRELATION COEFFICIENT: Measure of linear correlation between 2 variables X and Y.
+1 = 100% +ve correlation
-1 = 100% -ve correlation
0 = no correlation

For a population, Pearson correlation coefficient ρ = covariance(X, Y) / (σ_x * σ_y)
where cov(X,Y) = E[(X - μx)(Y - μy)]

PRACTICAL ISSUES:
1) Under heavy noise conditions, extracting ρ b/w 2 sets of stochastic variables is non-trivial.
2) In case of missing data, use the maximum likelihood estimator.
--------------------------------------
p-value is the probability of obtaining the observed results of a test, assuming that the null hypothesis is correct.

A result is said to be STATISTICALLY SIGNIFICANT if it allows us to reject the null hypothesis.

Intuitively & visually, referring to chart on wikipedia here, https://en.wikipedia.org/wiki/P-value
its the area under the probability density function (PDF) beyond the 95th percentile (typical value of α = 0.05)
 in the gaussian-distributed PDF.
ie, the event that an extremely unlikely event can occur under the null hypothesis.

NULL HYPOTHESIS IS REJECTED WHEN p-VALUE < α and not rejected when p > α

A 90% p-value for a feature in modeling means that there's 90% probability of this feature affecting the outcome y
is TOTALLY RANDOM, and not due to this feature being a predictor for y. Smaller the p-value, more significant the
results or greater the feature importance.
"""