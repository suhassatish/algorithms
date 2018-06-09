# -*- coding: utf-8 -*-
"""
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
P-VALUE is the probability for a given statistical model, that when the null hypothesis is true,
the statistical summary (such as sample mean difference b/w 2 compared groups) >= the actual observed results.

A result is said to be STATISTICALLY SIGNIFICANT if it allows us to reject the null hypothesis.

Intuitively & visually, referring to chart on wikipedia here, https://en.wikipedia.org/wiki/P-value
its the area under the probability density function (PDF) beyond the 95th percentile (typical value of α = 0.05)
 in the gaussian-distributed PDF.
ie, the event that an extremely unlikely event can occur under the null hypothesis.

NULL HYPOTHESIS IS REJECTED WHEN p-VALUE < α and not rejected when p > α


"""