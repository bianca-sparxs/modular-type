import cv2 as cv
import numpy as np
import cv2
import os



# imgdir = './cam'

tempdir = './test'

# I deleted the making letter code but keep it in the slice branch C.O

# 1. Use which method to do the template matching?, CCOEFF_NORM seems to be the constant(C.O)
# 2. How to cut the templates in to desire shape, You did that! :D 
# 3. The images have to be the same size for bitwise operations, for now, use monospace(C.O)


def create_match(temp, img, num, name, threshold=0.05):
    print("create_match num is " + str(num))
    dimX = temp.shape[1]
    dimY = temp.shape[0]


# the first element in the temp of TTop is 3 is that like alpha channel or something?
# I noticed that too... it's something like that, or maybe it stands for 3 colourspace (RGB)?
# also i love writing notes in the comments lol

    w = temp.shape[1]
    h = temp.shape[0]
    print('img shape {0}, temp shape {1}'.format(img.shape, temp.shape))
    # print('w,h: {0},{1}, {2}'.format(w,h, temp.shape))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img, temp, getattr(cv2, name))
    
    # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2) 
    minScore, maxScore, minLoc, maxLoc = cv2.minMaxLoc(result)
    duplicate = img.copy()

    if (name == "TM_SQDIFF_NORMED" ):
        loc = np.where( result <= threshold)  
        for pt in zip(*loc[::-1]): 
            duplicate = cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 
    else:
        loc = np.where( result >= threshold)  
        for pt in zip(*loc[::-1]): 
            cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 


    # loc = np.where( result >= threshold)  
    # for pt in zip(*loc[::-1]): 
    #     cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 

    print(result)

    # cv2.rectangle(duplicate, maxLoc, (maxLoc[0]+dimX, maxLoc[1]+dimY), (0, 255, 0), 1)
    print("{0}: \nThe min score:", minScore, "\nThe max score", maxScore, "\nThe min location:", minLoc,
          "\nThe max location:".format(name), maxLoc, "\n")
    # cv.imshow(name, duplicate)
    
    cv2.imwrite('temp_result/' + str(num) + 'a' + '.png', duplicate)
    # cv2.destroyAllWindows()
    # cv.waitKey(0)


def tmp_match(temp, img, num):
    # create_match(temp, img, "TM_CCOEFF", threshold=4*10**5)
    # create_match(temp, img, "TM_CCOEFF_NORMED", threshold=0.6)
    # create_match(temp, img, "TM_CCORR", threshold=0.75)
    # create_match(temp, img, "TM_CCORR_NORMED", threshold=0.9)
    # create_match(temp, img, "TM_SQDIFF", threshold=8*10**7)
    create_match(temp, img, num, "TM_SQDIFF_NORMED", threshold=0.7)

def process():
    pass


def match(imgdir):
    print("got to temp matching!")

    # img = cv.imread("./test/types2.jpg")
    # temp = cv.imread("./test/longbar.jpg")
    
    num = 0
    for filename in os.listdir(imgdir):
        if filename.endswith(".jpg"):
            print(filename)
            img = cv.imread("./cam/" + filename)
            for temp in os.listdir(tempdir):
                template = cv.imread("./test/" + temp)
                tmp_match(template, img, num+1)
                num +=1
                print("num is " + str(num))
        else:
            continue

    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2,2))
    # dilate = cv.dilate(img, kernel)
    # cv.imshow("what the fuck", dilate)
    # cv.waitKey(0)

    # run(24, 18)

# match(imgdir)