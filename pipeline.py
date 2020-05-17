from PIL import Image
import os
import glob
import grid_temp_match

# git with windows take one lol
#take in Image object from txt2img.py
def imgPipe(image_info, chararray):
    os.mkdir("cam")
    savepath = "./cam/img-1.jpg"
    image_info[0].save(savepath)

    imgdir = './cam'     # dir that stores the input image
    basename = 'img-*.jpg'      # name of the input image (
    filelist = glob.glob(os.path.join(imgdir, basename))

    count = 0

    for filenum, infile in enumerate(filelist):
        print(filenum)  # not rly useful
        print("ha")
        print(infile)   # not rly useful
        im = Image.open(infile)
        imgwidth, imgheight = im.size
        print('Image size is: %d x %d ' % (imgwidth, imgheight))    # the size of the input image
        height = imgheight // 1     # the number decides how many columns you want
        width = imgwidth // image_info[1]       # the number decides how many rows you want
        start_num = 0
        for k, piece in enumerate(crop(im, height, width), start_num):
            img = Image.new('RGB', (width, height), 255)
            img.paste(piece)
            # path = os.path.join("./cam/cam%d.jpg" % int(k + 1)) 
            path = os.path.join("./cam/" + chararray[count] + ".jpg")
            img.save(path)
            # os.rename(path, os.path.join("./cam/cam%d.jpg" % int(k + 1)))
            os.rename(path, os.path.join("./cam/img-" + chararray[count] + ".jpg"))
            count += 1
            # print(count)

    if os.path.exists(savepath):
        os.remove(savepath)

    return grid_temp_match.pipeline(imgdir)

    
    
    




def crop(im, height, width):
    imgwidth, imgheight = im.size
    for i in range(imgheight // height):
        for j in range(imgwidth // width):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            yield im.crop(box)
    

    
