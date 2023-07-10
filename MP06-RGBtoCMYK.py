# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận
from PIL import Image

#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# mở file hình = đường dẫn
filehinh = r'astley.png'
img =   cv2.imread( filehinh  , cv2.IMREAD_COLOR) 

# đọc ảnh = pillow
imgPIL = Image.open(filehinh)

# tạo khung ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển cmyk
cmyk    = Image.new ( imgPIL.mode , imgPIL.size )           # xanh da trời
cyan    = Image.new ( imgPIL.mode , imgPIL.size )           # đỏ tươi
magenta = Image.new ( imgPIL.mode , imgPIL.size )
yellow  = Image.new ( imgPIL.mode , imgPIL.size )
black   = Image.new ( imgPIL.mode , imgPIL.size )

#lấy kích thước ảnh
w = cmyk.size [0] 
h = cmyk.size [1]

#2 vòng for để qyét điểm ảnh
for x in range(w):
    for y in range(h):
        
        # giá trị màu tại pixel tọa độ (x,y)
        R , G , B = imgPIL.getpixel((x,y))
        b = np.uint8 (min( R , G , B))
       
        # gán giá trị màu cho từng kênh
        cyan.putpixel   ((x,y),(B,G,0))
        magenta.putpixel((x,y),(B,0,R))
        yellow.putpixel ((x,y),(0,G,R))
        black.putpixel  ((x,y),(b,b,b))
        
        # c# là rgb
        # python là bgr

# chuyển ảnh pillow -> opencv
ccv = np.array (cyan)
mcv = np.array (magenta)
ycv = np.array (yellow)
bcv = np.array (black)


# display image as a new window
cv2.imshow ('cyan channel'      , ccv)
cv2.imshow ('magenta channel'   , mcv)
cv2.imshow ('yellow channel'    , ycv)
cv2.imshow ('black channel'     , bcv)


#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey (0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 


