import cv2 as cv
import numpy as np
import cv2
import os
import math

# todo: clear temp_result and cam before 

# imgdir = './cam'

tempdir = './test'


# I deleted the making letter code but keep it in the slice branch C.O

# 1. Use which method to do the template matching?, CCOEFF_NORM seems to be the constant(C.O)
# 2. How to cut the templates in to desire shape, You did that! :D 
# 3. The images have to be the same size for bitwise operations, for now, use monospace(C.O)

def intersect(curr, point, twidth, theight):
    if curr == [0,0]:
        return False
    else:
        # print("curr0 is:" + str(curr[0]) + " curr1 is:" + str(curr[1]) + " point0 is:" + str(point[0]) + " point1 is:" + str(point[1]))
        if curr[0] + twidth < point[0] + 0.3*twidth:
            return False
        if curr[1] + theight < point[1]:
            return False

    return True

def confidence(pt, hotspots):
    #confidence = 0; 
    #for spot in hotspots: 
    #if euclidean distance of pt, spot > confidence:
    #confidence = euclid distance of pt, spot
    #return confidence

    return
        
def create_match(temp, img, num, key, dic, name, threshold):
    dimX = temp.shape[1]
    dimY = temp.shape[0]
    match_count = 0


# the first element in the temp of TTop is 3 is that like alpha channel or something?
# I noticed that too... it's something like that, or maybe it stands for 3 colourspace (RGB)?
# also i love writing notes in the comments lol

    w = temp.shape[1]
    h = temp.shape[0]
    # print('img shape {0}, temp shape {1}'.format(img.shape, temp.shape))
    # print('w,h: {0},{1}, {2}'.format(w,h, temp.shape))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    temp_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img, temp, getattr(cv2, name))
    
    # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2) 
    minScore, maxScore, minLoc, maxLoc = cv2.minMaxLoc(result)
    duplicate = img.copy()
    curr = [0,0]

    if (name == "TM_SQDIFF_NORMED" ):
        loc = np.where( result <= threshold)  
        for pt in zip(*loc[::-1]): 
            duplicate = cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 
    else:
        loc = np.where( result >= threshold)  
        for pt in sorted(zip(*loc[::-1])):
            # print(pt)
            if intersect(curr, pt, w, h):
                pass
            else:
                # if confidence(pt, hotspots ) > 5:
                match_count += 1
                # print(pt)
                curr = pt
                cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1)
           

    # print("times we've seen " + key + ": " + str(match_count))

    if match_count > dic[key]:
        dic[key] = match_count

    # loc = np.where( result >= threshold)  
    # for pt in zip(*loc[::-1]): 
    #     cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 

    # print(result)

    # cv2.rectangle(duplicate, maxLoc, (maxLoc[0]+dimX, maxLoc[1]+dimY), (0, 255, 0), 1)
    # print("{0}: \nThe min score:", minScore, "\nThe max score", maxScore, "\nThe min location:", minLoc,
    #       "\nThe max location:".format(name), maxLoc, "\n")
    # cv.imshow(name, duplicate)
    
    cv2.imwrite('temp_result/' + str(num) + 'a' + '.png', duplicate)
    # cv2.destroyAllWindows()
    # cv.waitKey(0)


def tmp_match(temp, img, num, key, dic):
    # create_match(temp, img, "TM_CCOEFF", threshold=4*10**5)
    create_match(temp, img, num, key, dic, "TM_CCOEFF_NORMED", threshold=0.75)
    # create_match(temp, img, "TM_CCORR", threshold=0.75)
    # create_match(temp, img, "TM_CCORR_NORMED", threshold=0.9)
    # create_match(temp, img, "TM_SQDIFF", threshold=8*10**7)
    # create_match(temp, img, num, "TM_SQDIFF_NORMED", threshold=0.01)

def process():
    pass


def match(imgdir, lettersize):
    num = 0
    matches = {}
    colunit = math.floor(lettersize[0] / 2)
    rowunit = math.floor(lettersize[1] / 3)
    #probably shoudln't we hardcoded but shwhatever:
    hotspots = [(0,0),(colunit, 0),(0,rowunit),(colunit, rowunit),(0,rowunit*2),(colunit,rowunit*2)]

    print(hotspots)
    # print(colunit)
    # print(rowunit)
    
    for filename in os.listdir(imgdir):
        if filename.endswith(".jpg"):
            # print(filename)
            img = cv.imread("./cam/" + filename)
            for temp in os.listdir(tempdir):
                if temp not in matches.keys():
                     matches[temp] = 0
                key = temp
                template = cv.imread("./test/" + temp)
                tmp_match(template, img, num+1, key, matches)
                num +=1
                # print("num is " + str(num))
        else:
            continue

    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2,2))
    # dilate = cv.dilate(img, kernel)
    # cv.imshow("what the fuck", dilate)
    # cv.waitKey(0)

    # run(24, 18)
    print(matches)

# match(imgdir)