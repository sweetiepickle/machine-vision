# Lê Bảo Khương - 2046123

import cv2
from PIL import Image       #thư viện pillow
import numpy as np

# tạo đường dẫn chứa file hình
filehinh = r'astley.png'

# đọc hình ảnh = opencv
img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

# đọc ảnh màu = pillow -> tính toán các giá trị
imgPIL = Image.open (filehinh)

#tạo 1 ảnh binary mới cùng kích thước + mode với imgPIL để chứa ảnh sau khi chuyển nhị phân
bin = Image.new ( imgPIL.mode , imgPIL.size )

##kích thước ảnh imgPIL
w = bin.size [0] 
h = bin.size [1]

# thiết lập giá trị ngưỡng
nguong = 130

# 2 vòng for
for x in range(w) :
    for y in range(h):
                
        # giá trị điểm ảnh tại từng pixel
        R , G , B = imgPIL.getpixel((x,y))
        
        # grayscale 
        gray = np.uint8 ( 0.2126 * R + 0.7152 * G + 0.0722 * B )
        
        # xác định ngưỡng giá trị 
        if ( gray < nguong ):
            bin.putpixel(( x , y ), ( 0 , 0 , 0 ))
        else :
            bin.putpixel(( x , y ), ( 255 , 255 , 255 ))
         
        
#chuyển ảnh từ pil sang opencv để hiển thị
anhnhiphan = np.array ( bin )

cv2.imshow ('original image'    , img        )    
cv2.imshow ('binary'            , anhnhiphan )

cv2.waitKey(0)
cv2.destroyAllWindows()  
