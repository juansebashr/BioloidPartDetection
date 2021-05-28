import fnmatch
import os
import shutil
import sys
import time
import uuid
import zipfile
from importlib import reload
from ImageGeneration import BlenderAPI as bld
reload(bld)

import bpy

"""Define a set of helper functions for the RenderInterface class"""

def finds(patterns, list):
    results = []
    for pattern in patterns:
        results.extend(find(pattern, list))

def find(pattern, list):
    result = []
    for item in list:
        if fnmatch.fnmatch(item, pattern):
            result.append(item)
    return result

def validate_and_extract_model(model):
    if not (len(model.namelist()) == 4 or len(model.namelist()) == 2):
        raise ValueError('model file not correct format!')
    if len(model.namelist()) == 4:
        if not set(['Bot.jpg', 'Bot.obj', 'Top.obj', 'Top.jpg']) == set(model.namelist()):
            raise ValueError('model file not correct format!')
        return ['Bot.obj', 'Bot.jpg', 'Top.obj', 'Top.jpg']
    if len(model.namelist()) == 2:
        if not (len(find('*.jpg', model.namelist())) == 1 and len(find('*.obj', model.namelist())) == 1):
            raise ValueError('model file not correct format!')
        return find('*.obj', model.namelist()) + find('*.jpg', model.namelist())


class RenderInterface(object):
    """
    Provides a high-level interface to the rendering engine (and the background
    generation as well hopefully)
    The main attribute of this interface is the BlenderRandomScene self.scene.
    This provides all the require methods to generate a random scene with
    the specified subject, with respect to the distributions on the random
    variables involved.
    """

    def __init__(self, num_images=None, resolution=412, samples=128):
        """
        :param num_images: number of images to render on render_all()
        """
        self.num_images = num_images
        self.scene = None
        self.setup_blender(resolution, samples)
        # self.logfile = 'blender_render.log'

    def setup_blender(self, resolution=412, samples=128):
        """setup
        To be called on the first time blender is launched. Performs clean-up and
        setup of the scene, and instantiates the BlenderRandomScene class that
        controls all rendering
        :return: None
        """
        C = bpy.context
        D = C.blend_data
        C.scene.render.engine = 'CYCLES'
        try:
            C.scene.cycles.device = 'GPU'
        except:
            print("Warning: CUDA device not detected, using CPU instead!", file=sys.stderr)

        # instantiate scene
        self.scene = bld.BlenderRandomScene(bpy.data.scenes[0])
        # delete the initial cube
        for obj in C.scene.objects:
            if obj.name == 'Cube':
                cube = bld.BlenderCube(reference=bpy.data.objects['Cube'])
                cube.delete()
                break
        # Fetch the camera and lamp
        cam = bld.BlenderCamera(bpy.data.objects['Camera'])
        self.scene.set_render(resolution, samples)
        self.scene.add_camera(cam)

        # Instantiate 2 layers
        coll2 = D.collections.new("Collection 2")
        C.scene.collection.children.link(coll2)

    def subject_in_scene(self, output_file):
        self.output_file = output_file
        self.scene.subject_from_scene()

    def load_subject(self, obj_path, texture_path, output_file, obj_path_bot=None, texture_path_bot=None):
        """
        Loads a single subject into the RandomScene
        :param obj_path:
        :param texture_path:
        :param output_file:
        :return:
        """
        # begin output redirection
        # open(self.logfile, 'a').close()
        # old = os.dup(1)
        # sys.stdout.flush()
        # os.close(1)
        # os.open(self.logfile, os.O_WRONLY)

        # print("RENDER INTERFACE: Loading subjects {}, {}".format(obj_path, obj_path_bot), file=sys.stderr)
        # print("RENDER INTERFACE: Loading textures {}, {}".format(texture_path, texture_path_bot), file=sys.stderr)
        self.output_file = output_file
        self.scene.load_subject_from_path(
            obj_path=obj_path, texture_path=texture_path, obj_path_bot=obj_path_bot, texture_path_bot=texture_path_bot)
        # print("RENDER INTERFACE: Finish loading subjects! ", file=sys.stderr)
        # print("\n", file=sys.stderr)

        # end output redirection
        # os.close(1)
        # os.dup(old)
        # os.close(old)

    def load_subjects(self, obj_path, texture_path, obj_path_bot, texture_path_bot, output_file):
        """
        Loads two subjects into the RandomScene
        :param obj_path:
        :param texture_path:
        :param obj_path_bot:
        :param texture_path_bot:
        :param output_file:
        :return:
        """
        # begin output redirection
        open(self.logfile, 'a').close()
        old = os.dup(1)
        sys.stdout.flush()
        os.close(1)
        os.open(self.logfile, os.O_WRONLY)

        print("BLENDER RENDER INTERFACE: Loading subjects from : \n {}, \n {}".format(obj_path, obj_path_bot),
              file=sys.stderr)
        print("BLENDER RENDER INTERFACE: Loading textures from : \n {}, \n {}".format(texture_path, texture_path_bot),
              file=sys.stderr)
        self.output_file = output_file
        self.scene.load_subject_from_path(
            obj_path=obj_path, texture_path=texture_path, obj_path_bot=obj_path_bot, texture_path_bot=texture_path_bot)
        print("BLENDER RENDER INTERFACE: Finish loading subjects! ", file=sys.stderr)
        print("\n", file=sys.stderr)

        # end output redirection
        os.close(1)
        os.dup(old)
        os.close(old)

    def load_from_model(self, model_path, output_file):

        self.output_file = output_file
        # check the model file
        if not model_path.lower().endswith('.model'):
            raise ValueError('file extension not wrong!')

        with zipfile.ZipFile(model_path, 'r') as model:
            files = validate_and_extract_model(model)
            # attempt to create a non-existent folder
            temp = os.path.join(output_file, str(uuid.uuid4()))
            if os.path.isdir(temp):
                raise ValueError('unique ID not unique!')  # Fatal
            os.mkdir(temp)
            model.extractall(temp)

        error_reading_file = False
        if len(files) == 4:
            bot_obj_path = os.path.join(temp, files[0])
            bot_texture_path = os.path.join(temp, files[1])
            top_obj_path = os.path.join(temp, files[2])
            top_texture_path = os.path.join(temp, files[3])
            try:
                self.load_subjects(top_obj_path, top_texture_path, bot_obj_path, bot_texture_path, output_file)
            except:
                error_reading_file = True
        elif len(files) == 2:
            obj_path = os.path.join(temp, files[0])
            texture_path = os.path.join(temp, files[1])
            try:
                self.load_subject(obj_path, texture_path, output_file)
            except:
                error_reading_file = True

        # this is really ugly, but it does the job - rendering it for the first
        # time loads the image into Blender's memory, removing the need to
        # have a persistent texture file
        if not error_reading_file:
            # start output redirection
            open(self.logfile, 'a').close()
            old = os.dup(1)
            sys.stdout.flush()
            os.close(1)
            os.open(self.logfile, os.O_WRONLY)
            # render
            self.scene.render_to_file(os.path.join(temp, 'pre-render.png'))
            # end output redirection
            os.close(1)
            os.dup(old)
            os.close(old)
        # we can now clean house
        shutil.rmtree(temp)

        if error_reading_file:
            raise IOError("Error reading model file contents!")
        return

    def change_output_file(self, new_output_file):
        self.output_file = new_output_file

    def set_attribute_distribution_params(self, *args):
        """
        Interface to the method with identical name in BlenderRandomScene:

        Description from BlenderRandomScene:
        Sets the parameter of the distribution of an attribute attr.
        param has to exist in the distribution that is is associated with
        attr. For instance, if attr is assigned a UniformCDist, and
        is asked to change the param "mu", this will throw a KeyError.

        :param args:
        :return:
        """
        self.scene.set_attribute_distribution_params(*args)

    def set_attribute_distribution(self, attr, params):
        """
        Interface to the method with identical name in BlenderRandomScene:

        Description from BlenderRandomScene:

        Sets the distribution of attribute specified by attr. params is
        a dictionary containing the following:

        - 'dist': str ( this gives the distribution name which will go
        into a lookup table in random_render.DistributionFactory, and will
        return a distribution object identified by the name. Look in
        RandomLib.random_render.py for a full list)
        - everything else will be a dict of kwargs that the constructor for
        the specified distribution expects.

        For instance, to assign a uniform distribution to lamp_energy with
        lower bound 500.0 and upper bound 1000.0. Since the constructor for
        UniformCDist is: "def __init__(self, l=None, r=None, **kwargs)", and
        DistributionFactory maps "UniformD" to that distribution, we should
        specify param as:
        {'dist':'UniformD', 'l':500.0, 'r':1000.0}

        :param attr:
        :param params:
        :return:
        """
        self.scene.set_attribute_distribution(attr, params)

    def render_all(self, dump_logs=False, visualize=False, verb=1, progress=False, dry_run=False):

        if dry_run:
            print("BLENDER RENDER INTERFACE : DRY RUN MODE \n")

        print("BLENDER RENDER INTERFACE : Rendering {} images to {} \n ".
              format(self.num_images, self.output_file), file=sys.stderr)

        for i in range(self.num_images):
            start = time.time()
            # **********************  RENDER N SAVE **********************
            render_path = os.path.join(self.output_file, 'render%d.png' % i)
            if dry_run:
                self.scene.scene_setup()
                continue
            self.scene.render_to_file(render_path)
            end = time.time()

            if verb == 1:
                print('BLENDER RENDER INTERFACE : Rendered image {} of {}. Elapsed time: {:.3f}s'.
                      format(i, self.num_images, end - start), file=sys.stderr)

        logs = self.scene.retrieve_logs()
        params = self.scene.give_params()

        if not os.path.isdir(os.path.join(self.output_file, 'stats')):
            os.mkdir(os.path.join(self.output_file, 'stats'))

        if dump_logs:
            import json
            dump_file = os.path.join(self.output_file, 'stats', 'randomvars_dump.json')
            with open(dump_file, "w+") as f:
                json.dump(logs, f, sort_keys=True, indent=4, separators=(',', ': '))
            dump_file = os.path.join(self.output_file, 'stats', 'randomparams_dump.json')
            with open(dump_file, "w+") as f:
                json.dump(params, f, sort_keys=True, indent=4, separators=(',', ': '))

        if visualize:
            print("Warning: Visualizing Stats is Deprecated. Another script will be added to visualize it separately!",
                  file=sys.stderr)

        return logs
