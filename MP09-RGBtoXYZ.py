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
xc= Image.new(imgPIL.mode,imgPIL.size)           
yc= Image.new(imgPIL.mode,imgPIL.size)           
zc= Image.new(imgPIL.mode,imgPIL.size)
xyzc= Image.new(imgPIL.mode,imgPIL.size)

#lấy kích thước ảnh
w= imgPIL.size[0] 
h= imgPIL.size[1]

#2 vòng for để quét điểm ảnh
for x in range(w):
    for y in range(h):
        
        # giá trị màu tại pixel tọa độ (x,y)
        R,G,B=imgPIL.getpixel((x,y))
        
        # lấy các giá trị màu r g b tính toán
        cx= np.uint8(0.4124564*R + 0.3575761*G + 0.1804375*B)
        cy= np.uint8(0.2126729*R + 0.7151522*G + 0.0721570*B)
        cz= np.uint8(0.0193339*R + 0.1191920*G + 0.9503041*B)
        
        # gán giá trị màu cho từng kênh
        xyzc.putpixel((x,y),(cz,cy,cx))
        xc.putpixel((x,y),(cx,cx,cx))
        yc.putpixel((x,y),(cy,cy,cy))
        zc.putpixel((x,y),(cz,cz,cz))
        
        # c# là rgb
        # python là bgr

# chuyển ảnh pillow -> opencv
xyzcv= np.array(xyzc)
xcv= np.array(xc)
ycv= np.array(yc)
zcv= np.array(zc)

# display image as a new window
cv2.imshow ('XYZ channel'  , xyzcv)
cv2.imshow ('X channel'    , xcv)
cv2.imshow ('Y channel'    , ycv)
cv2.imshow ('Zchannel'     , zcv)
#cv2.imshow ('hinh goc '   ,img)


#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey(0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 


