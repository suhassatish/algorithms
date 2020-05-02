"""
3D Object Detection w/ Population Augmentation + Multi-Scale CNN Feature Maps
Apr 21, 2020 (Deep Learning Study Group (San Francisco)) -
**********************************************************

1) "Improving 3D Object Detection through Progressive Population Based Augmentation" - https://arxiv.org/abs/2004.00831
Progressive Population Based Augmentation (PPBA).
PPBA learns to optimize augmentation strategies by narrowing down the search space and adopting the best parameters
discovered in previous iterations.

This paper uses genetic algorithms and is not based on auto-augmentation.

1 iteration = 3K steps;
All iterations have batch size = 64.
Search for 30 iterations for car category, 20 iterations for pedestrian / cyclist categories.

Waymo Open Dataset is recently released for 3D object detection. It has 20X more scenes than KITTI dataset &
20X more human-annotated objects per scene.

Data augmentation was critical to KITTI dataset since it was a small dataset.
The paper shows that data augmentation remains an important method for boosting model perf even in large-scale datasets.
The gains due to PPBA maybe as large as changing the underlying architecture, without any increase in inference cost.

For both StarNet and PointPillars on the Waymo Open Dataset, the same
training and inference setting4 as [22] is used. All trials are trained on the full
train set and validated on the 10% val split (4,109 samples). During the search,
we train the first iteration for 8,000 steps and the remaining iterations for 4,000
steps on StarNet with batch size 128. We reduce the training steps on PointPillars
by half in each iteration with batch size 64, since it converges faster. We perform
the search for 25 iterations on StarNet and for 20 iterations on PointPillars.

RandomFlip has a negative impact on heading prediction for both car and pedestrian.
-------------------------------------------------------------------------------------

Paper reading meeting notes -
Meeting attendees - presenter: Mohammad Reza; Cosmin Negruseri, Stephane Egly, Induja Chandrakumar,
Alexander Shim, Deek, Dzmitry Lazerka, Han Lee, Jon Ozbek, Max Grigorev, Saurabh Thapliyal, Tom Bishop,
Wojtek Czarnowski
*****************************
AlexNet in 2012 was v.successful DL model on image classification on imageNet (1M images public dataset)
due to data augmentation techniques.

Angle of rotation of an image is a famous data augmentation technique.
Cropping & zooming / choosing aspect ratio of sub region are other common perturbation techniques.

Then people realized there's a smarter way to choose them than randomly changing the above.

Auto-augment was 1st introduced in google paper, policyAugmentation. Lets have a reinforcement learning (RL)
agent that will be trained on the reward signal of model accuracy trained on perturbed images.
In this paper, they discover a fixed policy and apply the same for all the epochs. Policy discovered by the RL agent
is fixed for all the epochs.

In PPBA paper, each epoch finds an optimal policy. So different epochs can have different policies. This is the big
difference with the google auto-augment paper.
---------

Its a discrete optimization problem, so RL can be used. Even genetic algorithms can be used.

GlobalTranslateNoise - Add gaussian noise with mean 0.

FrustrumDroupout - Drops some LIDAR points. Does it mimic real world LIDAR artifacts? How to know which
portions of the image to drop? Ans: occlusion maybe 1 way.

OCCLUSION often occurs when two or more objects come too close and seemingly merge or combine with each other.
Image processing system with object tracking often wrongly track the occluded objects [6].
Sometimes, after occlusion, the system will wrongly identify the initially tracked object as a new object

----------
Hamiltonian cycles in a graph - can be solved as a genetic algorithm (GA) or as an RL problem. GA is computationally
less expensive.
Mutation and cross-over operations are the keys on this genetic algorithm paper - on how mutations are done.
  - Cosmin Negruseri (Staff MLE @ Pinterest, working on Homefeed Ranking).
------

Ω(Θ) = Mean Avg Precision = measure of goodness of the model (fitness of a particular gene).

algorithm 2 - instead of choosing all possible directions to climb up a hill,
just choose 2 directions.
----

16 trials - each worker is a model. 16 models trained separately over the epochs.

***************************************************************************************
2) Analysis & Applications of Multi-Scale CNN Feature Maps" -
https://medium.com/@mohammadrezasanatkar/analysis-and-applications-of-multi-scale-cnn-feature-maps-a6804bbac8

Convolutional filter encodes the location of a feature in an image.
The early layers of the conv layers, they have a smaller receptive field.

Resnet-50 is a backbone DL architecture for vision models.

Dilated convolutions work well for dense-prediction vision tasks like depth estimation, optical
flow.
How does this compare with single-shot models for objects of different sizes?
    This is not a replacement for those models. This is not a new model, its just a
    mathematical framework that gives you a tool. If cars 10m away from you are not
    being detected correctly, then you can try experimenting with this.


***************************************************************************************


"""