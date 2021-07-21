# A fast introduction to Classification, Object Detection, and Image Segmentation for custom problem

# Bioloid parts detection and tracking 

This repo provides all the needed files to perform and detection and tracking of different parts of a Bioloid robot using Yolov4 and algorithm.

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

Finally, the third one is `Detection&Tracking`, where is the custom trained Yolov4 model, was trained using the Darknet framework [3], it can be tested using this Colab Notebook [![Open in colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1Y-vpJqE-hDDNfgGG3iO7nBr2KDvvhFM7?usp=sharing)

Later it's been added a fourth directory called `Segmentation`, is a work in progress but already have implemented a semantic segmentation algorithm that works for the Bioloid parts 

## Usage

You can start using this repo files in any part of the project based on your needs, this tutorial follows the complete pipeline used.

### Setup blender environment and directories

As mentioned above, we use Blender to make all the Renders of all the differents parts on the Bioloid, for this we use the Blender API in Python called `bpi`, this is preloaded in the Blender Console and is not available outside of it, this forces to called the `.py` file directly from the console to run the script using this command

`exec(open("path_to_the_file").read())`

We recommend to use Blender in scripting mode to using easily the console.

Also this program also this program works by generating the renders of 1 or 2 pieces and save them in a directory, so if you want to use it to different classes, you'll have to do it one by one, so is better to have all the directories organized by classes previously. 

### Image Generation using Blender

The Image Generation is done to the Bioloid parts and the distractors individually calling the files `mainParts.py` and `mainDistractors.py`, using the `RenderInterface` to manage the scene in Blender and do the renders, all of the info are in the comments of the scripts and in the README files of each part of the project

There are 2 ways of loading the 3D models to use in the program, the first one (used in the `mainParts` file) is to use the `load_subject` or `load_subjects` methods, that load the object  and the texture from path, and `subject_in_scene` (used in the `mainDistractors` file) that allows the user to use configure manually the object in blender using the tools from the GUI, defining the texture manually, painting it, etc, and loading the object into the `RenderInterface`, using this last method is mandatory to have just one object in the scene.

### Image merging

The Image Merging part of the project is using only Python and the PIL library. We need a directory where differents backgrounds images are stored (the more the better). 

This script allows to merge this background images with the render of the objects and the distractors, and also obtain the labels of each generated image to do the detection and to do the segmentation. The detection label is a `.txt` file that contain in each line the class of  one of the objects in the image, and the coordinates of the box (x_center, y_center, width, height); the segmentation label contains a mask which have in the pixels corresponding to the object a different number identifying the class number.

This is being done using the `mainMerging.py` file, that (for merging the objects) can called 2 different methods, the first is `generate_for_all_objects` that is used when you want to generate the images with only a single class per image, resulting in a directory with just images of one class and one object in each image; and the `generate_for_all_directories` method, that allows to generate images with objects for random classes that are store in different directories (one per class) inside a mother directory, and then save them all in a final directory choosing the number of images that are generated and the number of class objects that will be in every image.

### Detection and tracking

The detection and tracking of the project is done using the YOLOv4 [model ](https://arxiv.org/abs/2004.10934), this was chosen because it is better to work with state-of-the-art models. The creators of YOLOv4 also create their own framework to test and train the model called darknet, unlike Tensorflow or Pytorch, is written in C and requires to be build using CMake, if you want to use it to train the model using Colab, follow [this](https://www.youtube.com/watch?v=nOIVxi5yurE&) tutorial, otherwise if you want to run it locally, you'll have to make sure to have CUDA and OPENCV (from binaries, not just as a python module) installed in your PC, to that follow [this](https://youtu.be/saDipJR14Lc) tutorial.

Is highly probable that problems appear in the installation and tuning of darknet, there mostly happens because of the definition of the [environment variables](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0) in the installation of CUDA (and cuDNN, that is a necessary add-on library if you want to work with deep learning models) and OPENCV, make sure you're using the default names of the environment variables.

For test the model using the trained weights, you can use the Colab mentioned above, or if you want to do it locally, is just to put the files in darknet directory and run a single command in the terminal, at the end of [this tutorial](https://youtu.be/saDipJR14Lc) is explained.

## References

1.  Wong MZ, Kunii K, Baylis M, Ong WH, Kroupa P, Koller S. 2019. Synthetic dataset generation for object-to-model deep learning in industrial applications. *PeerJ Computer Science* 5:e222 https://doi.org/10.7717/peerj-cs.222. The code of the project can be found in https://github.com/921kiyo/3d-dl
2.  The AI Guy, following his tutorials :). Here is his [youtube Channel](https://www.youtube.com/channel/UCrydcKaojc44XnuXrfhlV8Q)
3.  YOLO original creator - Darknet framework. Original repo here https://github.com/AlexeyAB/darknet
