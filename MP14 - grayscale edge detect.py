# Lê Bảo Khương - 2046123

import cv2
from PIL import Image       # thư viện pillow
import numpy as np
import math

filehinh = r'astley.png'

img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

#thư viện pillow đọc ảnh màu -> tính toán các giá trị
imgPIL = Image.open (filehinh)

#tạo ảnh cùng kích thước + mode với imgPIL để chứa ảnh 
avg = Image.new ( imgPIL.mode , imgPIL.size )
det = Image.new ( imgPIL.mode , imgPIL.size )

##kích thước ảnh imgPIL
w = det.size [0] 
h = det.size [1]

#2 vòng for để sử lí ảnh rgb thành ảnh grayscale theo phương pháp avg
for x in range(w) :
    for y in range(h):
                
        #giá trị điểm ảnh tại từng pixel
        R , G , B = imgPIL.getpixel((x,y))
        
        #grayscale = ( r + g + b) / 3
        gray = np.uint8 (( R + G + B ) / 3 )
        
        #gán giá trị mức xám cho ảnh xám
        avg.putpixel (( x , y ) , ( gray , gray , gray ))

# gía trị ngưỡng 
nguong = 130
        
# khai báo ma trận thay thế sobel
sobelx = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
sobely = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

#2 vòng for
for x in range(1,w-1) :
    for y in range(1,h-1):
        
        gx = 0
        gy = 0
        
        for i in range (x-1, x+2):
            for j in range (y-1, y +2):
                
                #giá trị điểm ảnh tại từng pixel
                Rd , Gd , Bd  = avg.getpixel((i,j))

                # nhân ma trận thay thế cho việc lấy vectơ gradient 
                gx+= Rd * sobelx[i-x+1,j-y+1]
                gy+= Rd * sobely[i-x+1,j-y+1]            
        
        # tính m
        m = abs(gx) + abs(gy)
        if m <= nguong:
            det.putpixel((x,y), (0,0,0))
        else :
            det.putpixel((x,y), (255,255,255))

                            
#chuyển ảnh từ pil sang opencv để hiển thị
imgdet = np.array(det)

#cv2.imshow ('original image'    , img )    
cv2.imshow ('Edge detect'         , imgdet )  

cv2.waitKey(0)
cv2.destroyAllWindows()  