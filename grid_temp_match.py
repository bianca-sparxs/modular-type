from PIL import Image
import cv2 as cv
import os
import glob
import time


def slice(im, height, width):
    """
    :param im: The input image
    :param height: The number of columns
    :param width: The number of rows
    :return: Crop the image to given dimensions
    """
    imgwidth, imgheight = im.size
    for i in range(imgheight // height):
        for j in range(imgwidth // width):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            yield im.crop(box)


def sliceLetters(name, imgdir, basename):
    """
    :param name: The name of the output file
    :param imgdir: The name of the directory the input file is in (pretty useless rn)
    :param basename: The name of the input file
    :return: Produce a directory full of sliced letter parts
    """
    os.mkdir(name)      # making the output directory
    filelist = glob.glob(os.path.join(imgdir, basename))

    for filenum, infile in enumerate(filelist):
        result = infile[:5]
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        # print('Image size is: %d x %d ' % (imgwidth, imgheight))    # the size of the input image
        height = imgheight // 5     # the number decides how many columns you want
        width = imgwidth // 4       # the number decides how many rows you want
        start_num = 0
        for k, piece in enumerate(slice(im, height, width), start_num):
            img = Image.new('RGB', (width, height), 255)
            img.paste(piece)
            path = os.path.join(name + "/" + result + "-%d.jpg" % int(k + 1))
            img.save(path)
            os.rename(path, os.path.join(name + "/" + result + "-%d.jpg" % int(k + 1)))


def compare(dir, thresh):
    """
    :param dir: The directory that stores template parts
    :param thresh: The threshold for template matching
    :param method: The template matching method
    :return:
    """
    inputs = []
    common = []
    maxScores = []
    maxScores_mir = []

    for (dirpath, dirnames, filenames) in os.walk(dir):
        inputs.extend(filenames)

    for temp_file in inputs:
        temp = cv.imread(dir + "/" + temp_file)
        temp_mirror = cv.flip(temp, 1)
        for img_file in inputs:
            img = cv.imread(dir + "/" + img_file)
            match_result = cv.matchTemplate(img, temp, cv.TM_CCORR_NORMED)
            match_result_mirror = cv.matchTemplate(img, temp_mirror, cv.TM_CCORR_NORMED)
            _, maxScore, _, _ = cv.minMaxLoc(match_result)
            _, maxScore_mir, _, _ = cv.minMaxLoc(match_result_mirror)
            # print(img_file + ": " + str(maxScore))
            # print(img_file + ": " + str(maxScore_mir) + "(mirror)")
            if maxScore not in maxScores:
                maxScores.append(maxScore)
            if maxScore_mir not in maxScores_mir:
                maxScores_mir.append(maxScore_mir)
            if thresh <= maxScore < 1.0:
                if temp_file not in common:
                    common.append(temp_file)
        # print("\n")

    # print("normal max score:", sorted(maxScores))
    # print("mirror max score:", sorted(maxScores_mir))


def pipeline(outDir):
    sliceLetters(outDir, "", "img-*.jpg")
    compare(outDir, 0.98)


if __name__ == "__main__":
    start = time.time()
    pipeline("templates")
    end = time.time()
    print("entire thing took", round(end - start, 3), "second(s)")



# basename = "img-*.jpg"
# imgdir = ''