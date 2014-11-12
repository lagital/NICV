from tkinter import *
from PIL import Image

class BinImage:
	
	def __init__(self, imgPath):
		img = Image.open(imgPath) # open colour image
		img = img.convert('1') # convert image to black and white
		self._binaredImg = binarize(img)

	def binarize(cls, img):
		binaredImg=[]
    	for i in range(img.size[0]):
        	tmp=[]
        	for j in range(img.size[1]):
            	if img.getpixel((i,j))[0]==255:
                	tmp.append(1)
            	else:
                	tmp.append(0)
        	bImg.append(tmp)
    	return binaredImg

    def compareWith(self, binImg, method):

    	if method == SPECPOINTS
    		result=1
    	else if method == WEAVE
    		result=1
    	return result

    def detectSpecPoints(self, binImg):
    	return 0

    def detectWeaves(self, binImg):
    	return 0

def skeletize(binImg):
	imgWidth=len(binImg)
    imgHeight=len(binImg[0])

    #удаление паттернов

    flag = 1
    while flag!=0: #удаляем, пока удалялся хотя бы один пиксель
    	for i in range(1,imgWidth-1):
        	for j in range(1,imgHeight-1):
        		flag = 0
            	if binImg[j][i] == 0: #если пиксель черный, то выделяем и
                	square[]		  #сверяем квадрат 3х3 с паттерном
                	for iPixelShift (x-1,x+2)
                 		for yPixelShift (y-1,y+2)
                			square.append(binImg[i][y])
                	if compareWithPatternSquares(square):
                		img[j][i]=1
                		flag += 1

    #удаление шума

    flag = 1
    while flag!=0: #удаляем, пока удалялся хотя бы один пиксель
    	flag = 0;
    	for i in range(1,imgWidth-1):
        	for j in range(1,imgHeight-1):

            	if binImg[j][i] == 0: #если пиксель черный, то выделяем и
                	square[]		  #проверяем квадрат 3х3 на шум
                	for iPixelShift (x-1,x+2)
                 		for yPixelShift (y-1,y+2)
                			square.append(binImg[i][y])
                	if compareWithNoise(square):
                		img[j][i]=1
                		flag += 1

def compareWithPatternSquares(square):
	t123457=[1,1,0,0,1,0]
    t013457=[1,1,1,0,0,0]
    t134567=[0,1,0,0,1,1]
    t134578=[0,0,0,1,1,1]
    t0123457=[1,1,1,0,0,0,0]
    t0134567=[1,0,1,0,0,1,0]
    t1345678=[0,0,0,0,1,1,1]
    t1234578=[0,1,0,0,1,0,1]

    flag = False

    tmpSquare=[square[1],square[2],square[3],square[4],square[5],square[7]]
    if tmpSquare == t123457:
    	flag = True
    tmpSquare=[square[0],square[1],square[3],square[4],square[5],square[7]]
    if tmpSquare == t013457:
        flag = True
    tmpSquare=[square[1],square[3],square[4],square[5],square[6],square[7]]
    if tmpSquare == t134567:
        flag = True
    tmpSquare=[square[1],square[3],square[4],square[5],square[7],square[8]]
    if tmpSquare == t134578:
        flag = True
    tmpSquare=[square[0],square[1],square[2],square[3],square[4],square[5],square[7]]
    if tmpSquare == t0123457:
        flag = True
    tmpSquare=[square[1],square[3],square[4],square[5],square[6],square[7],square[8]]
    if tmpSquare == t1345678:
        flag = True
    tmpSquare=[square[0],square[1],square[3],square[4],square[5],square[6],square[7]]
    if tmpSquare == t0134567:
        flag = True
    tmpSquare=[square[1],square[2],square[3],square[4],square[5],square[7],square[8]]
    if tmpSquare == t1234578:
        flag = True

    return flag

def compareWithNoise(square):

    patterns=[[1,1,1,1,0,1,1,1,1],
       [1,1,1,1,0,1,1,0,0],
       [1,1,1,0,0,1,0,1,1],
       [0,0,1,1,0,1,1,1,1],
       [1,1,0,1,0,0,1,1,1],
       [1,1,1,1,0,1,0,0,1],
       [0,1,1,0,0,1,1,1,1],
       [1,0,0,1,0,1,1,1,1],
       [1,1,1,1,0,0,1,1,0],
       [1,1,1,1,0,1,0,0,0],
       [0,1,1,0,0,1,0,1,1],
       [0,0,0,1,0,1,1,1,1],
       [1,1,0,1,0,0,1,1,0]]

    for i in patterns:
        if square == i:
            return True
        else
        	return False

