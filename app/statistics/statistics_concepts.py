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
"""