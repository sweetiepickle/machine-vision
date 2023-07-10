# Lê Bảo Khương - 2046123

#----------------------------------------------------------------------------------------------------------------------------------------------
# import libraries
import cv2
from PIL import Image       # pillow
import numpy as np
import matplotlib.pyplot as plt         # draw charts

#----------------------------------------------------------------------------------------------------------------------------------------------
# các hàm con
# def < tên hàm con > ( thông tin input )

# chuyển ảnh rgb sang grayscale
def gray_luminance (imgPIL):            #imgPIL là ảnh đc đọc = pillow
    
    #tạo 1 ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển gray
    luminance = Image.new ( imgPIL.mode , imgPIL.size )
    
    ##kích thước ảnh imgPIL
    w = luminance.size [0] 
    h = luminance.size [1]

    #2 vòng for
    for x in range(w) :
        for y in range(h):
                    
            #giá trị điểm ảnh tại từng pixel
            R , G , B = imgPIL.getpixel((x,y))
            
            #grayscale = ( r + g + b) / 3
            gray = np.uint8 ( 0.2126 * R + 0.7152 * G + 0.0722 * B )
            
            #gán giá trị mức xám cho ảnh xám
            luminance.putpixel (( x , y ) , ( gray , gray , gray ))
     
    return luminance

#----------------------------------------------------------------------------------------------------------------------------------------------
# tính giá trị histogram      
def Histogram(luminance):
    
    # khai báo 1 mảng 1 chiều chứa 256 phần tử
    # do mỗi pixel có giá trị trong khoảng 0 -255
    his = np.zeros(256)           # tạo mảng = numpy
    
    # kích thước ảnh
    w = luminance.size[0]
    h = luminance.size[1]
    
    for x in range(w):
        for y in range(h) :
            
            #lấy giá trị tại pixel tọa độ (x,y)
            gR , gG , gB = luminance.getpixel((x,y))
            
            # giá trị gray = phần từ thứ gray trong mảng his
            # phần từ thứ gray +1 giá trị
            his[gR] += 1        # ++
            
    return his 

#----------------------------------------------------------------------------------------------------------------------------------------------
#
def rgb (imgPIL):
    
    # khai báo 1 mảng 1 chiều chứa 256 phần tử
    # do mỗi pixel có giá trị trong khoảng 0 -255
    hisrgb = np.zeros  ((3,256))           # tạo mảng = numpy
    # ~ [[],[],[]]
    
    # kích thước ảnh
    w = imgPIL.size [0]
    h = imgPIL.size [1]
    
    for x in range(w):
        for y in range(h) :
            
            #lấy giá trị tại pixel tọa độ (x,y)
            R , G , B = imgPIL.getpixel ((x,y))
            
            # 
            hisrgb [0][R] += 1
            hisrgb [1][G] += 1
            hisrgb [2][B] += 1
            
    return hisrgb 

#----------------------------------------------------------------------------------------------------------------------------------------------
# draws charts

def charts (his,hisrgb) :
      
    plt.figure( 'Biểu đồ Histogram biểu thị mức xám' , figsize = (((7 , 5))) , dpi = 100)       # dpi = 100 : 1 inch sẽ có 100 dấu chấm
    trucX = np.zeros (256)          # trục X là 1 mảng 1 chiều 256 phần tử
    trucX = np.linspace (start = 0, stop = 256, num = 256)
    plt.plot(trucX, his , color = 'purple')
    plt.title('Biểu đồ Histogram')
    plt.xlabel('Giá trị mức xám')
    plt.ylabel('Số điểm cùng giá trị mức xám')
    
    plt.figure( 'Biểu đồ Histogram' , figsize = (((7 , 5))) , dpi = 100)       # dpi = 100 : 1 inch sẽ có 100 dấu chấm
    trucX = np.zeros (256)          # trục X là 1 mảng 1 chiều 256 phần tử
    trucX = np.linspace (start = 0, stop = 256, num = 256)
    plt.plot(trucX, hisrgb[0] , color = 'red')
    plt.plot(trucX, hisrgb[1] , color = 'green')
    plt.plot(trucX, hisrgb[2] , color = 'blue')
    plt.title('Biểu đồ Histogram')
    plt.xlabel('Giá trị màu')
    plt.ylabel('Số điểm cùng giá trị')
    plt.show()
    
    
#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# tải đường dẫn chứa file hình    
filehinh = r'bird_small.jpg'
img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

# đọc ảnh = pillow
imgPIL = Image.open(filehinh)

# chuyển sang ảnh mức xám
gray = gray_luminance(imgPIL)

# tính giá trị histogram
his = Histogram(gray)
hisrgb = rgb(imgPIL)
# chuyển ảnh pillow -> opencv
graycv = np.array (gray)
cv2.imshow ('Anh muc xam' , graycv)
cv2.imshow ('Anh mau' , img )

#hiển thị biểu đồ
charts(his,hisrgb)

#----------------------------------------------------------------------------------------------------------------------------------------------

cv2.waitKey(0)
cv2.destroyAllWindows()  