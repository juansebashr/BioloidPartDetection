"""
This is the main file for the generation of the images of the parts from the robot,
this is the files that you called from the blender console using the following command
exec(open("D:\\Documents\\PycharmProjects\\BioloidPartsDetection\\ImageGeneration\\mainDistractors.py").read())
"""
import os
import sys
import bpy

# Save the blender context using the variable C to manage in the console and to set
# that the images are with no background
C = bpy.context
C.scene.render.engine = 'CYCLES'
C.scene.render.film_transparent = True

# If the computer have Nvidia GPU available, use it
try:
    C.user_preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
    C.user_preferences.addons['cycles'].preferences.devices[0].use = True
except(ValueError, Exception):
    print("Warning: CUDA device not detected, using CPU instead!", file=sys.stderr)

# The direction of the module to import it in the %PATH
directory = 'D:\\Documents\\PycharmProjects\\BioloidPartsDetection'

if not (directory in sys.path):
    sys.path.append(directory)

import ImageGeneration.RenderInterface as Render

""" ************* User parameters for render ************* """
num_images = 100
obj_name = 'Plant'
render_folder = 'D:\\Documents\\PycharmProjects\\BioloidPartsDetection\\Render_Workspace\\Renders\\FlyingDistractorsPNG'

# Instantiate the RenderInterface class and call the subject_in_scene method to render a object already in blender
# scene (With it own texture or nodes)
RI = Render.RenderInterface(num_images=num_images)
RI.subject_in_scene(render_folder)

"""
RenderInterface has a BlenderRandomScene object that controls random variables responsible for the scene.
These random variables have distributions associated with them. Here we show how to render with the default 
distributions.

Setting distribution parameters.
One can change the distribution parameters of certain attributes in the rendering engine. 
This involves specifying the attribute that needs to be adjusted (as long as the attribute exists) and
then specifying the parameter to tune.

For instance num_lamps is varied according to the continuous uniform distribution U[l,r]. This makes l and r 
(the upper and lower bound of the U-distribution) tunable parameters. For lamp energy, this is a truncated 
normal with parameters: {mu: mean, sigmu: sigma/mu, l: lower bound, r: upper bound} and any of these can be tuned.
Here the camera radius is set to be far of the figure, that its for the final part in the picture does not appear 
cut off and to be 
"""
RI.set_attribute_distribution_params('num_lamps', 'mid', 6)
RI.set_attribute_distribution_params('lamp_energy', 'mu', 50.0)
RI.set_attribute_distribution_params('lamp_size', 'mu', 5.)
RI.set_attribute_distribution_params('camera_radius', 'mu', 25)
RI.set_attribute_distribution_params('camera_radius', 'l', 20)
"""
You could also change the distribution of an attribute entirely, by giving it a distribution name. This will 
be one of the distributions specified in ImageGeneration/RandomLib/random_render.py
The function signature is as follows: RI.set_attribute_distribution(attr_name, dist=dist_name, kwargs)
Where kwargs is a keyword argument dict of the required parameters for each distribution
"""
RI.set_attribute_distribution('lamp_energy', {'dist': 'UniformD', 'l': 0.0, 'r': 20.0})
RI.set_attribute_distribution_params('camera_loc', 'normals', 'XYZ')
RI.set_attribute_distribution_params('camera_loc', 'phi_sigma', 10.0)

# Calling render_all creates all the images in the render_folder
RI.render_all(dump_logs=False, visualize=True)

# And finally rename the files in the render folder for the name of the object
files_directory = os.listdir(render_folder)
i = 0
for file in files_directory:
    os.rename(os.path.join(render_folder, file), os.path.join(render_folder, obj_name + str(i) + '.png'))
    i = i + 1
