"""
LEARNING TO RANK ANSWERS TO NON-FACTOID QUESTIONS FROM WEB COLLECTIONS
Key ideas from seminal paper in Information retrieval on ranking web search results -
Published in 2011 by Stanford, Yahoo & Google researchers
~/Dropbox/Tech_extras/search_data_mining_adTech/learning_to_rank.pdf

4 sets of features go into ANSWER RANKING. These features are learnt by CLASS-CONDITIONAL GENERATIVE LEARNING
    1) Similarity Features
    2) Translation Features
    3) Density/Frequency Features
    4) Web Correlation Features

For a particular Question, Layer1 is ANSWER RETRIEVAL, its completely UNSUPERVISED learning.

Answer RANKING is the next step that is a DISCRIMINATIVE LEARNER.
-----------------------

3) FG3 or Density/Frequency Features - Measure the density and frequency of question terms in the answer text.
-----------------------

Evaluation metrics and measures -
1) Layer 1 - Retrieval Recall @ N
2) Layer 2 re-ranking Precision @ 1
3) Mean Reciprocal Rank (MRR)
4) Discounted Cumulative Gain (DCG)
"""