# Lê Bảo Khương - 2046123

import cv2
from PIL import Image       #thư viện pillow
import numpy as np

filehinh = r'astley.png'

img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

#thư viện pillow đọc ảnh màu -> tính toán các giá trị
imgPIL = Image.open (filehinh)

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
        
#chuyển ảnh từ pil sang opencv để hiển thị
anhmucxam = np.array ( luminance )

cv2.imshow ('original image'    , img )    
cv2.imshow ('grayscale'         , anhmucxam )

cv2.waitKey(0)
cv2.destroyAllWindows()  