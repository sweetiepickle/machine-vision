# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận
from PIL import Image
import math

#----------------------------------------------------------------------------------------------------------------------------------------------
# các hàm con
# def < tên hàm con > ( thông tin input )

def smth(imgPIL, a):
        
    # tạo 1 khung ảnh để chứa bitmap sau khi làm mượt
    muot= Image.new(imgPIL.mode, imgPIL.size)
    
    # lấy kích thước ảnh
    w= imgPIL.size[0] 
    h= imgPIL.size[1]   
    
    # quét từ x = a -> x = width  - a
    #         y = a -> y = height - a
    for x in range (a,w-a): 
        for y in range (a,h-a):
            
            rs= 0
            gs= 0
            bs= 0
            
            # quét các điểm trong mặt nạ
            for i in range (x-a,x+a+1):
                for j in range (y-a,y+a+1):
                    
                    # giá trị điểm ảnh tại từng pixel
                    R , G , B = imgPIL.getpixel((i,j))
                    
                    # cộng dồn giá trị
                    rs+= R
                    gs+= G
                    bs+= B
                    
            # tính trung bình cộng
            t= (2*a+1)*(2*a+1)
                
            rs= np.uint8 ( rs / t )
            gs= np.uint8 ( gs / t ) 
            bs= np.uint8 ( bs / t )            
            
            muot.putpixel((x,y),(bs,gs,rs))
            
    return muot 

#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# mở file hình = đường dẫn
filehinh= r'astley.png'
#filehinh= r'bird_small.jpg'
img= cv2.imread(filehinh,cv2.IMREAD_COLOR) 

# đọc ảnh = pillow
imgPIL= Image.open(filehinh)

# làm mượt ảnh
m3= smth(imgPIL,1)
m5= smth(imgPIL,2)
m7= smth(imgPIL,3)
m9= smth(imgPIL,4)

# chuyển ảnh từ pillow -> opencv
m3cv= np.array(m3)
m5cv= np.array(m5)
m7cv= np.array(m7)
m9cv= np.array(m9)

cv2.imshow('3x3',m3cv)
cv2.imshow('5x5',m5cv)
cv2.imshow('7x7',m7cv)
cv2.imshow('9x9',m9cv)

#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey (0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 
