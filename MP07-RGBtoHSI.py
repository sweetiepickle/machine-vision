# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận
from PIL import Image
import math


#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# mở file hình = đường dẫn
filehinh = r'astley.png'
img = cv2.imread( filehinh  , cv2.IMREAD_COLOR) 

# đọc ảnh = pillow
imgPIL = Image.open(filehinh)

# tạo khung ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển hsi
hsi         = Image.new ( imgPIL.mode , imgPIL.size )           
hue         = Image.new ( imgPIL.mode , imgPIL.size )           
saturation  = Image.new ( imgPIL.mode , imgPIL.size )
intensity   = Image.new ( imgPIL.mode , imgPIL.size )

#lấy kích thước ảnh
w = imgPIL.size [0] 
h = imgPIL.size [1]

#2 vòng for để quét điểm ảnh
for x in range(w):
    for y in range(h):
        
        # giá trị màu tại pixel tọa độ (x,y)
        R , G , B = imgPIL.getpixel((x,y))
        
        # lấy các giá trị màu r g b tính toán
               
        t1 = ((R - G) + (R - B))/2
        t2 = math.sqrt((G-B)*(R-B) + ((R - G)*(R - G))) 
        t3 = math.acos(t1/t2)
           
        # h = ?
        
        hh = 0 
        
        if B <= G:
            hh = t3
        else:
            hh = 2*math.pi - t3
            
        hh = np.uint8 (hh*180/math.pi)      
        
        # s = ?
        s = 1- (3*min ( R , G , B ))/(R+G+B)
        s = np.uint8 (s*255)
            
        # i = ?
        i = np.uint8 ( (R+G+B)/3)
        
        # gán giá trị màu cho từng kênh
        hsi.putpixel        ((x,y),(i,s,hh))
        hue.putpixel        ((x,y),(hh,hh,hh))
        saturation.putpixel ((x,y),(s,s,s))
        intensity.putpixel  ((x,y),(i,i,i))
        
        # c# là rgb
        # python là bgr

# chuyển ảnh pillow -> opencv
hsicv   = np.array (hsi)
hcv     = np.array (hue)
scv     = np.array (saturation)
icv     = np.array (intensity)

# display image as a new window
cv2.imshow ('hue channel'           , hcv)
cv2.imshow ('saturation channel'    , scv)
cv2.imshow ('intensity channel'     , icv)
cv2.imshow ('hsi channel'           , hsicv)
#cv2.imshow ('hinh goc '             ,img)


#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey (0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 


