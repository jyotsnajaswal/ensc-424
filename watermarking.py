import os,sys,math
from PIL import Image
import numpy as num
from pylab import *
pi = 3.14159265359

#this function will convert r, g, b to y, cb, cr
def _ycc(r, g, b): # in (0,255) range
    y  =  0.299*r +  0.587    *g +  0.114*b
    cb =  128     -  0.168736 *r -  0.331364*g + .5*b
    cr =  128     +  0.5      *r -  0.418688*g - .081312*b
    return y, cb, cr

#this function will convert y, cb, cr to r, g, b
def _rgb(y, cb, cr):
    r = y  +  1.402   * (cr-128)
    g = y  -  0.34414 * (cb-128)  -  0.71414 * (cr-128)
    b = y  +  1.772   * (cb-128)
    return r, g, b

#pass the matrix that you want to look at in the human readable form
def _file(variable):
	num.savetxt("yCompFile", variable, fmt='%-7.2f')

def _convert_into_picture(matrix):
	img = Image.fromarray(matrix.astype('uint8'))
	img.save('yComp.png')
	img.show()

def _zig_zag_scan(sizeX, sizeY, matrix):
        i = 0
        j = 0
        counter=0
        size= sizeX*sizeY
        zigzaglist = [0 for x in range (size)]
        #print(matrix)
        #print(zigzaglist)
        while ((i < sizeX)  and (j < sizeY)):
                zigzaglist[counter]= matrix[i][j]
                if (i == 0 and (j == 0 or (j%2==0))):
                        i=0
                        j=j+1
                elif(i==0 and j%2==1):
                        i=i+1
                        j=j-1
                elif(j==0 and i%2==0):
                        i=i-1
                        j=j+1
                elif(j==0 and 1%2==1):
                        i=i+1
                        j=0
                elif((i==0 or i%2==0) and j== sizeY-1):
                        i=i+1
                        j=j-1
                elif(i%2==1 and j==sizeY-1):
                        i=i+1
                        j=sizeY-1
                elif(i==sizeX-1 and (j==0 or j%2==0)):
                        i=i-1
                        j=j+1
                elif(i==sizeX-1 and j%2==1):
                        i=sizeX-1
                        j=j+1
                elif( (i+j) %2 ==0):
                        i=i-1
                        j=j+1
                elif((i+j)%2==1):
                        i=i+1
                        j=j-1

                counter = counter+1
        #print(zigzaglist)
        return zigzaglist

def _inverse_zig_scan(sizeX, sizeY, zigzaglist):
	i=0
	j=0
	zigzaglist =[ 0 for x in range (20)]
	#zigzaglist = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
	matrix = [[0 for x in range(n)]for y in range (m)]
	counter=0
	while ((i < sizeX)  and (j < sizeY)):                
		matrix[i][j]= zigzaglist[counter]
		if (i == 0 and (j == 0 or (j%2==0))):
		        i=0
		        j=j+1          
		elif(i==0 and j%2==1):
		        i=i+1
		        j=j-1            
		elif(j==0 and i%2==0):
		        i=i-1
		        j=j+1            
		elif(j==0 and 1%2==1):
		        i=i+1
		        j=0
		elif((i==0 or i%2==0) and j== sizeY-1):
		        i=i+1
		        j=j-1
		elif(i%2==1 and j==sizeY-1):
		        i=i+1
		        j=sizeY-1
		elif(i==sizeX-1 and (j==0 or j%2==0)):
		        i=i-1
		        j=j+1
		elif(i==sizeX-1 and j%2==1):
		        i=sizeX-1
		        j=j+1
		elif( (i+j) %2 ==0):
		        i=i-1
		        j=j+1
		elif((i+j)%2==1):
		        i=i+1
		        j=j-1
	counter = counter+1
	print(matrix)
	return(matrix)

def _DCT(sizeX, sizeY, y_matrix):
    sum1 = 0
    dct = num.empty((sizeX, sizeY), dtype=object)  

    for p in range(0,sizeX):
        for q in range(0,sizeY):
            if p==0:
                a_p = 1/(math.sqrt(sizeX))
            else:
                a_p = 2/(math.sqrt(sizeX))
            if q==0:
                a_q = 1/(math.sqrt(sizeY))
            else:
                a_q = 2/(math.sqrt(sizeY))
            for i in range(0, sizeX):
                    for j in range(0, sizeY):
                    	sum1 = sum1 + (y_matrix[i][j]*math.cos((2*i +1)*pi/(2*sizeX))*math.cos((2*j +1)*pi/(2*sizeY)))
            dct[p][q] = a_p*a_q*sum1
            print dct[p][q]
            sum1 = 0                                                                            
    #print(dct)
    return(dct) 

def _inverse_DCT(sizeX, sizeY, dct):
    sum1 = 0
    y_matrix = num.empty((sizeX, sizeY), dtype=object) 

    for p in range(0,sizeX):
        for q in range(0,sizeY):
            for i in range(0, sizeX):
                for j in range(0, sizeY):
                    if p==0:
                        a_p = 1/(math.sqrt(sizeX))
                    else:
                        a_p = 2/(math.sqrt(sizeX))
                    if q==0:
                        a_q = 1/(math.sqrt(sizeY))
                    else:
                        a_q = 2/(math.sqrt(sizeY))
                    sum1 = sum1 + (a_p*a_q*dct[i][j]*math.cos((2*i +1)*pi/(2*sizeX))*math.cos((2*j +1)*pi/(2*sizeY)))                    
                y_matrix[p][q] = sum1
                sum1 = 0                                                                            
	print(y_matrix)
	return(y_matrix)

def _ATM(yComp):
	print yComp
	row0 = len(yComp)
	column0 = len(yComp[0])
	print row0
	print column0
	arrTemp = num.empty((row0, column0), dtype=object)
	for row in range(0, row0): # loop through every pixel location
		for column in range(0, column0):
			xIndex = (2*column + row) % row0
			#print ("This is the x index : " + str(x))
			yIndex = (column + row) % row0
			#print ("This is the x index : " + str(y))
			arrTemp[x][y] = yComp[row][column]
	print arrTemp
	return arrTemp


if __name__ == "__main__":
	im = Image.open("pic.png")
	print ("Format of the Image:  " + str(im.format) + "Size of the Image: " + str(im.size) + "Mode of the image: " + str(im.mode))
	size   = im.size
	pixcel = im.load()
	#num.savetxt("orignalImage", pixcel, fmt='%-7.2f')
	arrYComp  = num.empty((size[0], size[1]), dtype=object)
	arrCbComp = num.empty((size[0], size[1]), dtype=object)
	arrCrComp = num.empty((size[0], size[1]), dtype=object)
	for x in range(0, size[0]):
		for y in range(0, size[1]):
			r, g, b, total        =  im.getpixel( (x, y) ) 
			arrayIs               =  pixcel[x,y]
			yComp, cbComp, crComp =  _ycc(r, g, b)
			arrYComp[x, y]        =  yComp
			arrCbComp[x, y]       =  cbComp
			arrCrComp[x, y]       =  crComp
	arrDCTComp = num.empty((size[0], size[1]), dtype=object)
	sizeX = len(arrYComp)
	sizeY = len(arrYComp[0])
	arrDCTComp = _DCT(sizeX, sizeY, arrYComp)
	_file(arrYComp)
	_convert_into_picture(arrYComp)
	_file(arrDCTComp)
	_convert_into_picture(arrDCTComp)
	#print _zig_zag_scan(size[0], size[1], arrYComp)
	#arrATMComp = _ATM(arrYComp)
	#_file(arrATMComp)
	#_convert_into_picture(arrATMComp)

