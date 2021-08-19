# import subprocess
import os
from os import makedirs, path
import shutil
import pathlib

pathToDataset = "../../../Twitch_dataset"
indexNumIm = -5
numNumbers = 4
periodInFrames = 30  # 2fps

folders = os.listdir(pathToDataset)

numVids = 0
indexIm = 0
currVidData = ""
currVidAnnotations = ""
lastImageName = ""

newImName = ""
newAnnotationName = ""

# make folder for txt files
pathlib.Path("ImageSets").mkdir(parents=True, exist_ok=True)
f = open("ImageSets/Twitch_vid.txt", "a")
t = open("ImageSets/Twitch_vid_test.txt", "a")

for folder in folders[:-1]:
    images = os.listdir(os.path.join(pathToDataset, folder, "image"))[:-1]
    for image in images:

        if (indexIm == 0) or (
                previousImageName != "" and (int(previousImageName[indexNumIm]) + 1) % 10 != int(image[indexNumIm])):
            # make new folder for video data
            currVidData = path.join("Data/VID", "%04d" % (numVids,))  # f"{numVids:04d}"
            pathlib.Path(currVidData).mkdir(parents=True, exist_ok=True)

            # make new folder for annotations
            currVidAnnotations = path.join("Annotations/VID", "%04d" % (numVids,))
            pathlib.Path(currVidAnnotations).mkdir(parents=True, exist_ok=True)

            numVids += 1
            indexIm = 0

        # copy and rename images and annotations

        shutil.copyfile(path.join(pathToDataset, folder, "image", image), path.join(currVidData, image))
        newImName = "%06d" % (indexIm * periodInFrames,) + ".JPEG"
        os.rename(path.join(currVidData, image), path.join(currVidData, newImName))

        annotationName = image[:indexNumIm + 1] + ".xml"
        shutil.copyfile(path.join(pathToDataset, folder, "image_annotation", annotationName),
                        path.join(currVidAnnotations, annotationName))
        newAnnotationName = "%06d" % (indexIm * periodInFrames,) + ".xml"
        os.rename(path.join(currVidAnnotations, annotationName), path.join(currVidAnnotations, newAnnotationName))

        if (numVids < 2000):
            f.write("%04d" % (numVids - 1,) + " 1 " + str(indexIm * periodInFrames) + " " + str(165) + '\n')
        else:
            t.write("%04d" % (numVids - 1,) + " 1 " + str(indexIm * periodInFrames) + " " + str(165) + '\n')

        indexIm += 1

        previousImageName = image
