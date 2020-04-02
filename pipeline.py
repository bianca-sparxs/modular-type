from PIL import Image
import os
import glob


def crop(im, height, width):
    imgwidth, imgheight = im.size
    for i in range(imgheight // height):
        for j in range(imgwidth // width):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            yield im.crop(box)


if __name__ == '__main__':
    imgdir = './cam'     # dir that stores the input image
    basename = 'img-*.jpg'      # name of the input image (
    filelist = glob.glob(os.path.join(imgdir, basename))
    for filenum, infile in enumerate(filelist):
        print(filenum)  # not rly useful
        print(infile)   # not rly useful
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        print('Image size is: %d x %d ' % (imgwidth, imgheight))    # the size of the input image
        height = imgheight // 1     # the number decides how many columns you want
        width = imgwidth // 5       # the number decides how many rows you want
        start_num = 0
        for k, piece in enumerate(crop(im, height, width), start_num):
            img = Image.new('RGB', (width, height), 255)
            img.paste(piece)
            path = os.path.join("./cam/cam%d.jpg" % int(k + 1))
            img.save(path)
            os.rename(path, os.path.join("./cam/cam%d.jpg" % int(k + 1)))
