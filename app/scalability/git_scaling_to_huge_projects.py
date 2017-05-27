"""
https://blogs.msdn.microsoft.com/bharry/2017/05/24/the-largest-git-repo-on-the-planet/
Notes from above blog:

1) Virtualizing .git folder and the working directory allows git to scale to very large projects.

2) Rather than downloading the whole repo and checkout all the files, GVFS (git virtual file system)
dynamically downloads only the portions you need based on what you use.

3) Windows code base is live on git. It has 3.5 Million files and when checked-in, results in a repo
of 300 GB (vs 4 GB Castlight SOA code base including checked-in jar files).
4k engineers in windows producing about 1,760 daily "lab builds" across 440 branches + 1ks of pull
request validation builds.

Windows has very large merges across branches with 10ks of changes with 1ks of conflicts.

4) LIsts had to be virtualized so that the UI didn't hang at that scale.

5) For globally distributed teams in low bandwidth regions, git proxy solution caches data
"at the edge".

"""