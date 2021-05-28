import os
directory = "D:\\Documents\\PycharmProjects\\darknet\\data\\Finals\\Validation\\"
image_files = []
for i in range(len(os.listdir(directory))):
    files_directory = os.path.join(directory,os.listdir(directory)[i])
    for filename in os.listdir(files_directory):
        if filename.endswith(".jpg"):
            image_files.append("data/Finals/Validation/" + os.listdir(directory)[i]+'/'+filename)
    #os.chdir("..")
with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()
os.chdir("..")