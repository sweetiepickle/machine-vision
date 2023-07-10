# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận
from PIL import Image
import math


#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# mở file hình = đường dẫn
filehinh= r'astley.png'
img= cv2.imread(filehinh,cv2.IMREAD_COLOR) 

# đọc ảnh = pillow
imgPIL= Image.open(filehinh)

# tạo khung ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển hsi
ycbcrc= Image.new(imgPIL.mode,imgPIL.size)           
yc= Image.new(imgPIL.mode,imgPIL.size)           
crc= Image.new(imgPIL.mode,imgPIL.size)
cbc= Image.new(imgPIL.mode,imgPIL.size)         

#lấy kích thước ảnh
w= imgPIL.size[0] 
h= imgPIL.size[1]

#2 vòng for để quét điểm ảnh
for x in range(w):
    for y in range(h):
        
        # giá trị màu tại pixel tọa độ (x,y)
        R,G,B=imgPIL.getpixel((x,y))
        
        # lấy các giá trị màu r g b tính toán
        cy= np.uint8(16+(65.738*R)/256 + (129.057*G)/256 + (25.064*B)/256)
        cb= np.uint8(128-(37.945*R)/256 - (74.494*G)/256 + (112.439*B)/256)
        cr= np.uint8(128+(112.439*R)/256 - (94.154*G)/256 - (18.285*B)/256)
        
        # gán giá trị màu cho từng kênh
        ycbcrc.putpixel((x,y),(cr,cb,cy))
        yc.putpixel((x,y),(cy,cy,cy))
        cbc.putpixel((x,y),(cb,cb,cb))
        crc.putpixel((x,y),(cr,cr,cr))
        
        # c# là rgb
        # python là bgr

# chuyển ảnh pillow -> opencv
ycbcrcv= np.array(ycbcrc)
ycv= np.array(yc)
cbcv= np.array(cbc)
crcv= np.array(crc)

# display image as a new window
cv2.imshow ('YCrCb channel'  , ycbcrcv)
cv2.imshow ('Y channel'    , ycv)
cv2.imshow ('Cr channel'    , cbcv)
cv2.imshow ('Cb channel'     , crcv)
#cv2.imshow ('hinh goc '   ,img)


#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey(0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 


