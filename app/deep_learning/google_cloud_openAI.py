"""
Brown bag by Allister Lundberg (Jiff) on Aug 2, 2017

OpenAI is good for reinforcement learning algorithms.

Google cloud is 10-50% cheaper than AWS with comparable performance, but reduced features.
Google cloud has VMs.
DataProc is Apache Spark + little bit of extra stuff
GoogleML is batch ML. Queue-based. 5 mins wait-time for Q to be free. 15 mins-30 mins it takes.
Not so good for interactive training like optimizing hyper parameters or experimenting with many
algorithms.

TPUs (tensor processing unit) are massively parallel GPUs. In alpha right now, not public.
"gcloud" is cmdline

$100-$150/month spent. 16 CPUs, 104 GB Memory

Private repositories storage are free now for beta.

TF-learn is not so good yet. Keras is simplified way to interact with tensor flow.

OpenAI is open source for reinforcement learning.
----------------------
Deep Q Network (DQN) - Simplest form of Reinforcement Learning. Given internal state, whats optimal
state?
3 layers. 1st 2 layers are 64 nodes. 3rd layer pops out Q value.
"""