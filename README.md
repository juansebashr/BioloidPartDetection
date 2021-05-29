# Bioloid parts detection and tracking 

This repo provides all the needed files to perform and detection and tracking of different parts of a Bioloid robot using Yolov4 and Deepsort algorithm.

## Libraries

This project requires the following libraries

- Numpy

- OpenCV

- PIL

- Sys

- Fnmtach

- Tensorflow

- Keras

- Random

- Colorsys

- resizeimage 

In the files there are more import modules, but there are blender modules that are preinstalled in the Python Blender console

## Organization 

This project is organized in 3 phases (which each one of them are put in a different directory), the first one is called `ImageGeneration` where all the synthetic images of the dataset are build using Blender 2.92 and a modified Blender API [1] to generate a bunch of images from different perspectives and with different lighting conditions of any .obj file with texture, more information in the README of the directory.

The second one is called `ImageMerging` where are the code to take the previous PNG image generated without background and merge them in a random position for a background dataset, and at the same time making the label from training the Yolov4 model. In our project we use 2 types of image to merge with the background, the renders of the differents parts of the model and a bunch of "Flying distractors" [2] that are use to give variety to final images, more information in the README of the directory.

Finally, the third one is `Detection&Tracking`, where is the custom trained Yolov4 and Deepsort model, was trained using the Darknet framework and deployed using Tensorflow [3], it can be tested using this Colab Notebook [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Y-vpJqE-hDDNfgGG3iO7nBr2KDvvhFM7?usp=sharing)


## Usage

You can start using this repo files in any parse of the project based on your needs, this tutorial follows the complete pipeline used.

### Setup blender environment and directories

As mentioned above, 



## References

1.  Wong MZ, Kunii K, Baylis M, Ong WH, Kroupa P, Koller S. 2019. Synthetic dataset generation for object-to-model deep learning in industrial applications. *PeerJ Computer Science* 5:e222 https://doi.org/10.7717/peerj-cs.222. The code of the project can be found in https://github.com/921kiyo/3d-dl
2. asdfsd
3. 

https://github.com/AlexeyAB/darknet

A huge thanks to team of  
