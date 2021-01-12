"""
https://www.youtube.com/watch?v=yXxGOcVomGM
DeText: A Deep NLP Framework for Intelligent Text Understanding
talk by LinkedIn on Oct 19, 2020 on
Wei Wei Guo - Sr Mgr @ LinkedIn NLP group

https://engineering.linkedin.com/blog/2020/open-sourcing-detext

Slides @ ~/Dropbox/tech_extras/nlp/linkedin-deText-nlp-Oct2020/

Challenge for BERT serving - ~30X slower than CNN
Large param space, 12-layer google BERT has 110M params.

Real-time inference computation grows linearly with # of documents.

2 pass ranking - soln to large # of documents
1st pass - MLP model uses traditional features only
2) top ranked docs are sent to more complex models
------

Document texts rarely change, mostly static. So generate document embeddings offline and cache them for online
    consumption. Inference cost is mostly reduced from computation cost to N/W cost to fetch from distributed caches.



"""