import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt #Drawing diagram library

def main():
    #Image path
    imgor = r'astley.png'
    #Read Image
    img = cv2.imread(imgor, cv2.IMREAD_COLOR)
    #Read color image using PIL library, which can replace OpenCV to process image
    imgPIL = Image.open(imgor)
    #Assign value for image
    lumpic_tem = RGBLuminaceConvert(imgPIL)
    threshold = OtsuMultiThreshold(lumpic_tem)
    print("ngưỡng k1 : ", threshold[0])
    print("ngưỡng k2 : ", threshold[1])
    Segimg = HisSegment(lumpic_tem, threshold)
    #Histogram Calculation
    hisPIL = HistogramCalculation(lumpic_tem)
    #Convert PIL to opencv to show in opencv library
    graypic = np.array(lumpic_tem)      
    #Show Image
    cv2.imshow('Luminace Grayscale Image', graypic)
    cv2.imshow('Original Image', img)
    cv2.imshow('Segmented Image', Segimg)   
    HistogramDiagram(hisPIL)
    #Bấm phím bất kì để đóng cửa sổ
    cv2.waitKey()
    #Quit key
    cv2.destroyAllWindows()
   
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
    #lumpic = np.array(lum)
    return lum

#Tính Histogram của ảnh xám
#Khai báo mảng chứa 256 phần tử chứa điểm ảnh
def HistogramCalculation(graypicPIL):
    his = np.zeros(256) #1-D matrix has 256 components
    #Get Image dimension
    w = graypicPIL.size[0]
    h = graypicPIL.size[1]
    for x in range(w):
        for y in range(h):
            #Get grayscale value at position (x,y)
            gR, gG, gB = graypicPIL.getpixel((x,y))
            his[gR] += 1
    return his

#Vẽ biểu đồ Histogram GrayScale dùng thư viện Matplotlib
def HistogramDiagram(his):
    w = 5
    h = 4
    plt.figure("Histogram Diagram of Grayscale Image", figsize=((w,h)), dpi = 100)
    Xaxis = np.zeros(256)
    Xaxis = np.linspace(0, 256, 256)
    plt.plot(Xaxis, his, color = 'orange')
    plt.title("Histogram Diagram")
    plt.xlabel("Grayscale value")
    plt.ylabel("Points have the same value of grayscale")
    plt.show()
    
#  phương pháp Otsu : tính toán ngưỡng sao cho tổng phương sai giữa hai lớp được phân tách là lớn nhất.
def OtsuMultiThreshold(imgPILGray):
    # Create cumulative arrays
    VarB = np.zeros((256,256))
    VarB_max = 0
    threshold = np.zeros(2)
    # Tinh histogram
    his = HistogramCalculation(imgPILGray)

    width = imgPILGray.size[0]
    height = imgPILGray.size[1]

    # Tần suất xuất hiện của các pixel có cùng mức xám pi ( i in range 256 )
    p = his/(width*height)
    #Compute the global intensity mean mG
    mG = sum(i*p[i] for i in range(256))
    
    
    #Compute VarG
    VarG = sum(p[i]*((i - mG)**2) for i in range(256))

    for k1 in range(256):
        for k2 in range(k1, 256):
            # cumulative sum
            P1 = sum(p[i] for i in range(k1))
            P2 = sum(p[i] for i in range(k1+1, k2))
            P3 = sum(p[i] for i in range(k2+1, 256))
            if(P1 == 0 or P2 == 0 or P3 == 0):
                continue
            # cumulative avg
            m1 = sum(i*p[i] for i in range(k1))/P1
            m2 = sum(i*p[i] for i in range(k1, k2))/P2
            m3 = sum(i*p[i] for i in range(k2, 256))/P3
            
            
            
            
            #Compute the between-class variance
            VarB = P1*(m1 - mG)**2 + P2*(m2 - mG)**2 + P3*(m3 - mG)**2          
                       
            if VarB > VarB_max:
                VarB_max = VarB
                threshold[0] = k1
                threshold[1] = k2
            #Compute n
            n = VarB_max/VarG
    print("độ chính xác : ", n)
    return threshold
 
def HisSegment(imgPIL, threshold):
    #Make a copy of imgPIL to return the converted image
    sgmimg = Image.new(imgPIL.mode, imgPIL.size)
    #Take the image dimension
    width = sgmimg.size[0]
    height = sgmimg.size[1]
    #Each picture is a 2-dimension matrix so we'll use 2 for loops to read all of the pixels in each picture
    for x in range(width):
        for y in range(height):
            #Get value of pixel at each position
            r, g, b = imgPIL.getpixel((x,y))
            #calculate the grayscale
            gray = np.uint8(0.2126*r + 0.7152*g + 0.0722*b)
            #Identify the segment value
            if (gray < threshold[0]):
                #Assign the 255 value for image
                sgmimg.putpixel((x, y), (0, 0, 0))
            if(gray > threshold[0] and gray < threshold[1]):
                #Assign the 255 value for image
                sgmimg.putpixel((x, y), (100, 100, 100))
            if(gray > threshold[0] and gray > threshold[1]):
                #Assign the RGB value for image
                sgmimg.putpixel((x, y), (255, 255, 255))
    sgmpic = np.array(sgmimg)
    return sgmpic

main()