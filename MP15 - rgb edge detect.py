# Lê Bảo Khương - 2046123

import cv2
from PIL import Image       #thư viện pillow
import numpy as np
import math

filehinh = r'astley.png'

img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

#thư viện pillow đọc ảnh màu -> tính toán các giá trị
imgPIL = Image.open (filehinh)

#tạo ảnh cùng kích thước + mode với imgPIL để chứa ảnh 
det = Image.new ( imgPIL.mode , imgPIL.size )

##kích thước ảnh imgPIL
w = det.size [0] 
h = det.size [1]

# gía trị ngưỡng 
nguong = 130
        
# tạo ma trận thay thế sobel
sobelx = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
sobely = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

#2 vòng for
for x in range(1,w-1) :
    for y in range(1,h-1):
        
        gxr = 0
        gxg = 0 
        gxb = 0
            
        gyr = 0 
        gyg = 0     
        gyb = 0
        
        for i in range (x-1, x+2):
            for j in range (y-1, y +2):
                
                #giá trị điểm ảnh tại từng pixel
                R , G , B  = imgPIL.getpixel((i,j))

                gxr+= R * sobelx[i-x+1,j-y+1]
                gxg+= G * sobelx[i-x+1,j-y+1]
                gxb+= B * sobelx[i-x+1,j-y+1]
                
                gyr+= R * sobely[i-x+1,j-y+1]
                gyg+= G * sobely[i-x+1,j-y+1]
                gyb+= B * sobely[i-x+1,j-y+1]            
        
        gxx = gxr**2 + gxg**2 + gxb**2
        gyy = gyr**2 + gyg**2 + gyb**2
        gxy = gxr*gyr + gxg*gyg + gxb*gyb
        
        theta = np.arctan2((2*gxy),(gxx - gyy)) * 1/2 
        
        f0 = np.sqrt((gxx+gyy)/2 + (gxx - gyy)*math.cos(2*theta) + 2*gxy*math.sin(2*theta))
        
        if f0 >= nguong:
            det.putpixel((x,y), (255,255,255))        
        else:
            det.putpixel((x,y), (0,0,0))        

                            
#chuyển ảnh từ pil sang opencv để hiển thị
imgdet = np.array(det)

#cv2.imshow ('original image'    , img )    
cv2.imshow ('Edge detect'         , imgdet )  

cv2.waitKey(0)
cv2.destroyAllWindows()  