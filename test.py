# _*_ coding: utf-8 _*_
from sklearn import neighbors


neighbors.KNeighborsClassifier()

import cv2
import numpy as np
import urllib2
from matplotlib import pyplot as plt

opener = urllib2.build_opener()
p_url = "http://wl.tjportnet.com/cas/simpleImg?uuid=76bc04b0-d3d1-4d2c-82b7-c0996e6cdb7a25"
pic = opener.open(p_url)
content = pic.read()
f = open('a.png', 'wb')
f.write(content)
f.close()


img = cv2.imread("a.png", 0)
# hist, bins = np.histogram(img.ravel(), 256, [0, 256])
# cdf = hist.cumsum()

plt.hist(img.ravel(), 256)

print img.shape
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        if img[i][j] < 220:
            img[i][j] = 0
cv2.namedWindow("Image")
cv2.imshow("Image", img)


kernel = np.ones((2, 3), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
cv2.imshow("Image2", erosion)

# plt.plot(cdf)
img = cv2.imread('a.png',0) #直接读为灰度图像
#简单滤波
ret1,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#Otsu 滤波
ret2,th2 = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
print ret2
plt.figure()
plt.subplot(221),plt.imshow(img,'gray')
plt.subplot(222),plt.hist(img.ravel(),256)#.ravel方法将矩阵转化为一维
plt.subplot(223),plt.imshow(th1,'gray')
plt.subplot(224),plt.imshow(th2,'gray')
plt.show()
cv2.waitKey(0)