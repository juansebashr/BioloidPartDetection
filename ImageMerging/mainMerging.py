"""
Created May 09 of 2021

@author: Sebastian Hernandez

This is the main file to run for merging the render images from the different classes, the
flying distractors and the background. Finally it add noise to the images

"""
import ImageMerging as Merge

from importlib import reload

reload(Merge)
base_address = "D:\\Documents\\PycharmProjects\\BioloidPartsDetection\\Render_Workspace"


Merge.mergeDistractors.merge_all_distractors(base_address + "\\Renders\\FlyingDistractorsPNG",
                                             base_address + "\\BgDatabase\\Tables",
                                             base_address + "\\ImageMerging\\DistractorsBG",
                                             n_of_images=200, img_size=416)

bbox = Merge.mergeBackground.generate_for_all_objects(base_address + "\\Renders\\ManoPNG",
                                                      base_address + "\\ImageMerging\\DistractorsBG",
                                                      base_address + "\\Prueba", n_of_pixels=416,
                                                      adjust_brightness=False)
keys = list(bbox.keys())
for key in keys:
    name = key[:-4]
    f = open(base_address + "\\Finals\\Mano\\" + name + ".txt", "w+")
    f.write(str(6) + " " + str(bbox[key][0]) + ' ' + str(bbox[key][1]) +
            ' ' + str(bbox[key][2]) + ' ' + str(bbox[key][3]))
    f.close()
