import os
import random
import shutil

folder = "D:\\Documents\\PycharmProjects\\BioloidPartsDetection\\Render_Workspace\\Finals\\Training\\Pechera"
folder2 = "D:\\Documents\\PycharmProjects\\BioloidPartsDetection\\Render_Workspace\\Finals\\Validation\\Pechera"
directory = os.listdir(folder)

for ele in directory:
    if ele[-4:] == '.txt':
        directory.remove(ele)

random.shuffle(directory)

validation = directory[-int(len(directory)*0.2):]

for image in validation:
    shutil.move(os.path.join(folder,image),os.path.join(folder2,image))
    shutil.move(os.path.join(folder, image[:-4]+'.txt'),os.path.join(folder2,image[:-4]+'.txt'))