"""
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
Notes from Leah McGuire talk (SFDC PMTS Einstein)
https://www.youtube.com/watch?time_continue=570&v=Eh802ZeAcC4

1) item-item similarity recommenders are more stable and scalable than user-item similarity.
2) Matrix factorization methods and item-item similarity approaches work better than restricted boltzmann machines.

"""