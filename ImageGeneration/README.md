# Image Generation

This is the Image Generation package of the project, here are the files for the Blender management, the definitions of the Random Distributions that follows the camera positions and the light conditions of the scene, and the integration in a Interface that allows to automate the control of the rendering, to get the renders in a specific directory.

Is designed to run in Blender version 2.8 or superior.

To run it you have 2 options, open Blender without the GUI, using the terminal in Linux or Windows; the second option is open Blender with the GUI as it is normally done, and then open the blender console inside the GUI.

Having done that, is important to note that the Python that is running in the Blender console is not the Python you download normally in your PC, this is a specific distribution that is downloaded with blender, and serves to run Blender within it, it have already some built-in modules include the module `bpy`, is imported usually in the `BlenderAPI` and the `RenderInterface` to control the Blender Context, it documentation is found [here](https://docs.blender.org/api/current/index.html).



