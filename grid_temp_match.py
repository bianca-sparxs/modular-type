from PIL import Image, ImageOps
import cv2 as cv
import os
import glob
import time
import shutil


outDir = "slicers"

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
        height = imgheight // 3     # the number decides how many columns you want
        width = imgwidth // 2       # the number decides how many rows you want
        start_num = 0
        for k, piece in enumerate(slice(im, height, width), start_num):
            img = Image.new('RGB', (width, height), 255)
            img.paste(piece)
            path = os.path.join(name + "/" + result + "-%d.jpg" % int(k))
            img.save(path)
            os.rename(path, os.path.join(name + "/" + result + "-%d.jpg" % int(k)))


def compare(dir, thresh):
    """
    :param dir: The directory that stores template parts
    :param thresh: The threshold for template matching
    :return: List of parts that can patch letters together
    """
    num = 0
    inputs = []
    letter_list = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    parts_list = {k: [0,1,2,3,4,5] for k in letter_list}     # List of parts for letters

    shutil.copytree(dir, "lib")     # Library for the templates
    for (dirpath, dirnames, filenames) in os.walk(dir):
        inputs.extend(filenames)

    needed = inputs.copy()

    for temp_file in inputs:
        temp = cv.imread(dir + "/" + temp_file)
        temp_mirror = cv.flip(temp, 1)      # Flip the template horizontally
        candidates = {}
        print("\nloop",num)

        for img_file in inputs:
            img = cv.imread(dir + "/" + img_file)

            if temp_file == img_file:
                continue
            else:
                match_result = cv.matchTemplate(img, temp, cv.TM_CCORR_NORMED)
                match_result_mirror = cv.matchTemplate(img, temp_mirror, cv.TM_CCORR_NORMED)
                _, maxScore, _, _ = cv.minMaxLoc(match_result)
                _, maxScore_mir, _, _ = cv.minMaxLoc(match_result_mirror)

                if maxScore > thresh:
                    candidates[temp_file+":"+img_file] = maxScore

                if maxScore_mir > thresh:
                    candidates["mir-"+temp_file+":"+img_file] = maxScore_mir

        # print(candidates)
        for key in candidates:
            if key.split(":")[0][0:3] == "mir":
                if key.split(":")[0][4:] in needed:
                    if key.split(":")[1] in needed:
                        # print("what is about to be removed:",key.split(":")[1])
                        # print("\nthis is the letter:", key.split(":")[1][4], ", and this is the part:", int(key.split(":")[1][6]))
                        parts_list[key.split(":")[1][4]][int(key.split(":")[1][6])] = key.split(":")[0]
                        needed.remove(key.split(":")[1])
                        os.remove("lib/" + key.split(":")[1])
                        # print(key.split(":")[1], "is removed")

            if key.split(":")[0] in needed:
                if key.split(":")[1] in needed:
                    # print("what is about to be removed:",key.split(":")[1])
                    # print("\nthis is the letter:", key.split(":")[1][4], ", and this is the part:",
                    #       int(key.split(":")[1][6]))
                    parts_list[key.split(":")[1][4]][int(key.split(":")[1][6])] = key.split(":")[0]
                    needed.remove(key.split(":")[1])
                    os.remove("lib/"+key.split(":")[1])
                    # print(key.split(":")[1],"is removed")

        # print("what is left:", needed)
        num += 1

    # print(parts_list)
    # shutil.rmtree(dir)
    # shutil.rmtree("lib")
    fuck = parts_list
    return parts_list


def pipeline(letterDir):
    """
    :param outDir: The directory that contains all the sliced parts
    :param letterDir: The directory that contains all the letters
    :param thresh: The thresh for template matching
    :return parts_list: List of parts that can patch letters together
    """
    thresh=0.9
    sliceLetters(outDir, letterDir, "img-*.jpg")
    parts_list = compare(outDir, thresh)
    return parts_list



def patch(letter, parts_dict, img_dir):
    empty = Image.new('RGB', (320, 444))
    current_wid = 0
    current_hei = 0
    # parts_list = parts_dict[letter]
    # for i in range(6):
    #     if type(parts_list[i]) == int:
    #         img = Image.open(img_dir + "/img-" + letter + "-" + str(parts_list[i])+ ".jpg")
    #         empty.paste(im=img, box=(current_wid, current_hei))
    #         print("current loc:", (current_wid, current_hei))
    #         current_wid += 160
    #         current_hei += 148
    #         if current_wid > 160:
    #             current_wid = 0
    #     elif parts_list[i][0:3] == "mir":
    #         img = Image.open(img_dir+"/"+parts_list[i][4:])
    #         img = ImageOps.mirror(img)
    #         empty.paste(im=img, box=(current_wid, current_hei))
    #         print("current loc:", (current_wid, current_hei))
    #         current_wid += 160
    #         current_hei += 148
    #         if current_wid > 160:
    #             current_wid = 0
    #     else:
    #         img = Image.open(img_dir+"/"+parts_list[i])
    #         empty.paste(im=img, box=(current_wid, current_hei))
    #         print("current loc:", (current_wid, current_hei))
    #         current_wid += 160
    #         current_hei += 148
    #         if current_wid > 160:
    #             current_wid = 0

    img2 = Image.open("lib/img-X-1.jpg")
    img1 = ImageOps.mirror(img2)
    img3 = Image.open("lib/img-X-2.jpg")
    img4 = ImageOps.mirror(img3)
    img5 = Image.open("lib/img-X-4.jpg")
    img6 = ImageOps.mirror(img5)

    # img1 = Image.open("lib/img-E-0.jpg")
    # img2 = Image.open("lib/img-E-1.jpg")
    # img3 = Image.open("lib/img-E-2.jpg")
    # img4 = Image.open("lib/img-E-3.jpg")
    # img5 = Image.open("lib/img-E-4.jpg")
    # img6 = Image.open("lib/img-E-5.jpg")

    empty.paste(im=img1, box=(0,0))
    empty.paste(im=img2, box=(160,0))
    empty.paste(im=img3, box=(0,148))
    empty.paste(im=img4, box=(160,148))
    empty.paste(im=img5, box=(0,296))
    empty.paste(im=img6, box=(160,296))

    empty.save("what.jpg")


# if __name__ == "__main__":
#     # start = time.time()
#     result = pipeline(, "")
#     # end = time.time()
#     # print("\nentire thing took", round(end - start, 3), "second(s)")
#     # patch("A", fuck, "lib")

