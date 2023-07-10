# Lê Bảo Khương - 20146123

import cv2
from PIL import Image       #thư viện pillow
import numpy as np

filehinh = r'astley.png'

img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

#thư viện pillow đọc ảnh màu -> tính toán các giá trị
imgPIL = Image.open (filehinh)

#tạo 1 ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển gray
lightness = Image.new ( imgPIL.mode , imgPIL.size )

##kích thước ảnh imgPIL
w = lightness.size [0] 
h = lightness.size [1]

#2 vòng for
for x in range(w) :
    for y in range(h):
                
        #giá trị điểm ảnh tại từng pixel
        R , G , B = imgPIL.getpixel((x,y))
        
        #grayscale = ( min + max ) / 2
        MIN = min ( R , G , B )
        MAX = max ( R , G , B )
        gray = np.uint8 ( ( MIN + MAX) / 2 )
        
        #gán giá trị mức xám cho ảnh xám
        lightness.putpixel (( x , y ) , ( gray , gray , gray ))
        
#chuyển ảnh từ pil sang opencv để hiển thị
anhmucxam = np.array ( lightness )

cv2.imshow ('original image'    , img )    
cv2.imshow ('grayscale'         , anhmucxam )

cv2.waitKey(0)
cv2.destroyAllWindows()  