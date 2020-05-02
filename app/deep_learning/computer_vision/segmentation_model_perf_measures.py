"""
Meetup on Apr 29, 2020 - Computer Vision Models for Object Detection
https://www.meetup.com/aittg-sfsv/events/270205342
-----------------
Model Performance Measures for Bounding Box Segmentation problems -

1)
Take predicted rectangle & ground truth rectangle, then compute IoU, ie:
area of intersection / area of Overlap


2) Average Precision (AP) - combines precision, recall, IoU and some simple integrals.
Provies a measure of how well a model is predicting classes of objects

3) Avg Precision across scales

4) Avg Recall (AR)

5) AR across scales
----
reference datasets -
CIFAR-10, COCO,

------
GluonCV


"""