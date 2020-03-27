import cv2 as cv
import numpy as np
import cv2


def run(row, col):
    pic_A = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_B = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_C = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_D = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_E = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_F = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_G = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_H = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_I = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_J = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_K = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_L = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_M = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_N = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_O = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_P = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_Q = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_R = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_S = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_T = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_U = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_V = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_W = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_X = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_Y = np.zeros(shape=[row, col], dtype=np.uint8)
    pic_Z = np.zeros(shape=[row, col], dtype=np.uint8)

    # for i in range(len(pic_A)):
    #     for j in range(len(pic_A[0])):
    #         pic_A[i][j] = 255
    #         pic_B[i][j] = 255
    #         pic_C[i][j] = 255
    #         pic_D[i][j] = 255
    #         pic_E[i][j] = 255
    #         pic_F[i][j] = 255
    #         pic_G[i][j] = 255
    #         pic_H[i][j] = 255
    #         pic_I[i][j] = 255
    #         pic_J[i][j] = 255
    #         pic_K[i][j] = 255
    #         pic_L[i][j] = 255
    #         pic_M[i][j] = 255
    #         pic_N[i][j] = 255
    #         pic_O[i][j] = 255
    #         pic_P[i][j] = 255
    #         pic_Q[i][j] = 255
    #         pic_R[i][j] = 255
    #         pic_S[i][j] = 255
    #         pic_T[i][j] = 255
    #         pic_U[i][j] = 255
    #         pic_V[i][j] = 255
    #         pic_W[i][j] = 255
    #         pic_X[i][j] = 255
    #         pic_Y[i][j] = 255
    #         pic_Z[i][j] = 255

    # How to produce "A"

    for i in range(len(pic_A)):
        for j in range(len(pic_A[0])):
            if j == 0 or j == col - 1:
                pic_A[i][j] = 0
            if i == 0:
                pic_A[i][j] = 0
            if i == 3:
                pic_A[i][j] = 0

    # How to produce "X"
    # for i in range(len(pic_X)):
    #     for j in range(len(pic_X[0])):
    #         if i == j:
    #             pic_X[i][j] = 0

    # How to produce "C"
    for i in range(len(pic_C)):
        for j in range(len(pic_C[0])):
            if i == 0 or i == len(pic_C) - 1:
                pic_C[i][j] = 0
            if j == 0:
                pic_C[i][j] = 0

    # How to produce "B"
    for i in range(len(pic_B)):
        for j in range(len(pic_C[0])):
            if i == 0 or i == len(pic_B) - 1:
                pic_B[i][j] = 255
            if j == 0 or j == len(pic_C[0]) - 1:
                pic_B[i][j] = 255
            if i == len(pic_B) // 2 - 1:
                pic_B[i][j] = 255

    # cv.imwrite("letter_C.jpg", pic_C)
    # cv.imwrite("letter_A.jpg", pic_A)
    cv.imwrite("letter_B.jpg", pic_B)
    # cv.imwrite("letter_c.jpg", pic_C)
    # cv.imwrite("letter_c.jpg", pic_C)


# 1. Use which method to do the template matching?
# 2. How to cut the templates in to desire shape
# 3. The images have to be the same size for bitwise operations
# 4.
def create_match(temp, img, name, threshold=0.05):
    dimX = temp.shape[1]
    dimY = temp.shape[0]


# the first element in the temp of T-Top is 3— is that like alpha channel or something?
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

    loc = np.where( result >= threshold)  
    for pt in zip(*loc[::-1]): 
        cv2.rectangle(duplicate, pt, (pt[0] + w, pt[1] + h), (0,0,255), 1) 

    print(result)


    # cv2.rectangle(duplicate, maxLoc, (maxLoc[0]+dimX, maxLoc[1]+dimY), (0, 255, 0), 1)
    print("{0}: \nThe min score:", minScore, "\nThe max score", maxScore, "\nThe min location:", minLoc,
          "\nThe max location:".format(name), maxLoc, "\n")
    cv.imshow(name, duplicate)
    # cv.imshow(name, img_gray)
    cv.waitKey(0)


def tmp_match(temp, img):
    create_match(temp, img, "TM_CCOEFF", threshold=4*10**5)
    create_match(temp, img, "TM_CCOEFF_NORMED", threshold=0.5)
    # create_match(temp, img, "TM_CCORR", threshold=0.75)
    # create_match(temp, img, "TM_CCORR_NORMED", threshold=0.75)
    # create_match(temp, img, "TM_SQDIFF", threshold=8*10**7)
    create_match(temp, img, "TM_SQDIFF_NORMED", threshold=0.99)

def process():
    pass


if __name__ == "__main__":
    pass
    # template = cv.imread("letter_A.jpg")
    # image = cv.imread("letter_B.jpg")
    # canvas = np.zeros(shape=[48, 36], dtype=np.uint8)
    # image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    # # cv.imshow("fuck", canvas)
    # # cv.waitKey(0)
    # # canvas = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
    # result = cv.bitwise_and(canvas, canvas, mask=image)
    # cv.imshow("w", result)
    # cv.waitKey(0)
    # tmp_match(template, image)

    img = cv.imread("./test/types2.jpg")
    temp = cv.imread("./test/longbar.jpg")
    tmp_match(temp, img)
    # kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (2,2))
    # dilate = cv.dilate(img, kernel)
    # cv.imshow("what the fuck", dilate)
    # cv.waitKey(0)

    # run(24, 18)