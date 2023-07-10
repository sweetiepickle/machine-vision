import numpy as np
import cv2
from PIL import Image

def main():
    while True:
        #Image path
        imgor = r'astley.png' 
        #Read Image
        img = cv2.imread(imgor, cv2.IMREAD_COLOR)
        #Read color image using PIL library, which can replace OpenCV to process image
        imgPIL = Image.open(imgor)
        edimg_tem = GrayscaleImageEdgeDetecting(imgPIL, 50)
        hello = np.array(edimg_tem)
        # Dilate the image using the circle structuring element
        dilated_image = np.array(dilate_made(edimg_tem, 1))
        eroded_image = np.array(erode_made(edimg_tem, 1))
        opening_image = np.array(opening_made(edimg_tem, 1))
        closing_image = np.array(closing_made(edimg_tem, 1))

        #Show original image
        cv2.imshow('Original Image', hello)
        
        #Show eroded image
        cv2.imshow('Eroded Image', eroded_image)
        #Show dilated image
        cv2.imshow('Dilated Image', dilated_image)
        #Show opening image
        cv2.imshow('Opening Image', opening_image)
        #Show closing image
        cv2.imshow('Closing Image', closing_image)
        
        #Quit key
        if cv2.waitKey(0): break
    cv2.destroyAllWindows()

def create_mask(radius):
    # Create a square array with side length 2 * radius + 1
    size = 2*radius + 1
    center = radius
    struct_elem = np.zeros((size, size), dtype=np.uint8)
    list = []
    a = 0
    # Set pixels within the radius of the center to 1
    for i in range(size):
        for j in range(size):
            # euclidean distance
            if (i - center)**2 + (j - center)**2 <= radius**2:
                struct_elem[i, j] = 1
                a = a + 1
    list = [struct_elem, a]
    # print (list)
    return list #2D numpy array

def erode_made(edimg, radius):
    # a matrix with size(512,512) comes from 0 to 511 pixels
    edimg_tem = Image.new(edimg.mode, edimg.size)    
    img_width = edimg_tem.size[0]
    img_height = edimg_tem.size[1]
    
    list = create_mask(radius)
    number = list[1]    # 5
    
    # Iterate over each pixel in the input image
    for width in range(radius, img_width - radius): #maximum is 511 - radius(2) = 509
        for height in range(radius, img_height - radius):
            # Create a mask matrix
            Rs = 0
            count = 0
            # width height : 1 - 5
            for i in range(width - radius, width + radius + 1): #509 - 2 + 1 + 2
                for j in range(height - radius, height + radius + 1):
                    mask = list[0]
                    
                    r, g, b = np.uint8(edimg.getpixel((i,j))) #.getpixel returns int value
                    Rs = r * mask[i -  (width - radius), j - (height - radius)]
                    #Erosion algorithm
                    if(Rs != 0):
                        count = count + 1   
                        if(count == number):
                            edimg_tem.putpixel((width, height), (Rs, Rs, Rs))
    return edimg_tem

def dilate_made(edimg, radius):
    edimg_tem = Image.new(edimg.mode, edimg.size)
    #Take the image dimension
    img_width = edimg_tem.size[0]
    img_height = edimg_tem.size[1]
    list = create_mask(radius)
    # Iterate over each pixel in the input image
    for width in range(radius, img_width - radius):
        for height in range(radius, img_height - radius):
            #Create a maskmatrix
            Rs = 0
            count = 0
            for i in range(width - radius, width + radius + 1):
                for j in range(height - radius, height + radius + 1):
                    a = list[0]
                    mask = a
                    #Get information R-G-B at the pixel point in mask at postion [i, j]
                    r, g, b = np.uint8(edimg.getpixel((i,j))) #.getpixel returns int value
                    Rs = r * mask[i -  (width - radius), j - (height - radius)]
                    #Dilation algorithm
                    if(Rs != 0):
                        edimg_tem.putpixel((width, height), (Rs, Rs, Rs))          
    return edimg_tem

def opening_made(edimg, radius):
    opening_img_tem = erode_made(edimg, radius)
    opening_img = dilate_made(opening_img_tem, radius)
    return opening_img

def closing_made(edimg, radius):
    closing_img_tem = dilate_made(edimg, radius)
    closing_img = erode_made(closing_img_tem, radius)
    return closing_img              

def RGBLuminaceConvert(imgPIL):
    #Make a copy of imgPIL to return the converted image
    lum = Image.new(imgPIL.mode, imgPIL.size)
    #Take the image dimension
    width = lum.size[0]
    height = lum.size[1]
    #Each picture is a 2-dimension matrix so we'll use 2 for loops to read all of the pixels in each picture
    for x in range(width):
        for y in range(height):
            #Get value of pixel at each position
            r, g, b = imgPIL.getpixel((x,y))
            #Using Lightness method with following equation
            gray = np.uint8(0.2126*r + 0.7152*g + 0.0722*b) #Using np.uint8 to convert the value to usigned integer 8bit (byte in C#)
            #Assign the gray value for avg 
            lum.putpixel((x, y), (gray, gray, gray))
    return lum 

def GrayscaleImageEdgeDetecting(imgPIL, threshold):
    edimg_tem = Image.new(imgPIL.mode, imgPIL.size)
    width = edimg_tem.size[0] 
    height = edimg_tem.size[1]
    
    for x in range(1, width - 1): #0 -> width - 1
        for y in range(1, height - 1):
            #Create a maskmatrix in g(x)
            maskx = np.zeros((512,512), np.int8) #Create a matrix has 512 components with datatype is integer 8 bit
            maskx[x - 1, y - 1] = -1; maskx[x - 1, y] = 0; maskx[x - 1, y + 1] = 1
            maskx[x, y - 1] = -2; maskx[x, y] = 0; maskx[x, y + 1] = 2
            maskx[x + 1, y - 1] = -1; maskx[x + 1, y] = 0; maskx[x + 1, y + 1] = 1
            #----------------------------------------------#
            #Create a maskmatrix in g(y)
            masky = np.zeros((512,512), np.int8) #Create a matrix has 512 components with datatype is integer 8 bit
            masky[x - 1, y - 1] = -1; masky[x - 1, y] = -2; masky[x - 1, y + 1] = -1
            masky[x, y - 1] = 0; masky[x, y] = 0; masky[x, y + 1] = 0
            masky[x + 1, y - 1] = 1; masky[x + 1, y] = 2; masky[x + 1, y + 1] = 1
            #Create variable to contain incremental value of pixel in mask. So they must be declared
            #"int" type to be able to contain those value.
            #Proceed to scan the points in the mask
            grayx = 0
            grayy = 0
            # rgb to grayscale 
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    
                    r, g, b = imgPIL.getpixel((i,j))
                    gray = np.uint8(0.2126*r + 0.7152*g + 0.0722*b) # luminance grayscale
                    #Calculate the Edge Dectecting funtion in g(x)
                    grayx += gray * maskx[i, j]
                    #Calculate the Edge Dectecting funtion in g(y)
                    grayy += gray * masky[i, j]
                    
            # grayscale to binary
            M = abs(grayx) + abs(grayy)
            if (M <= threshold):
                #Set image pixel
                edimg_tem.putpixel((x, y), (0,0,0)) #put 0 channel first, then 1 and 2 respectively
            else:
                #Set image pixel
                edimg_tem.putpixel((x, y), (255, 255, 255)) #put 0 channel first, then 1 and 2 respectively
    #edimg = np.array(edimg_tem)
    #edimg = np.array(edimg_tem)
    return edimg_tem

main()