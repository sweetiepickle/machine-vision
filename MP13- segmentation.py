# Lê Bảo Khương - 2046123

import cv2
from PIL import Image       # thư viện pillow
import numpy as np

filehinh = r'astley.png'

img = cv2.imread (filehinh , cv2.IMREAD_COLOR)

#thư viện pillow đọc ảnh màu -> tính toán các giá trị
imgPIL = Image.open (filehinh)

#tạo 1 ảnh cùng kích thước + mode với imgPIL để chứa ảnh sau khi phân đoạn
seg = Image.new ( imgPIL.mode , imgPIL.size )

# kích thước ảnh imgPIL
w = seg.size [0] 
h = seg.size [1]

# gía trị ngưỡng 
x1 = 80
x2 = 150    
y1 = 400
y2 = 500
nguong = 45

ravg = 0
gavg = 0
bavg = 0


#2 vòng for 
for x in range(x1,x2) :
    for y in range(y1,y2):
                
        #giá trị điểm ảnh tại từng pixel
        R , G , B = imgPIL.getpixel((x,y))
        
        # các giá trị cộng dồn từng kênh chứa trong vec tơ a
        ravg += R
        gavg += G   
        bavg += B
        
size = np.abs(x2 - x1) * np.abs(y2 - y1)
# chia trung bình các giá trị cộng dồn
ravg /= size
gavg /= size
bavg /= size
       
for x in range (w):
    for y in range (h):
        rz , gz , bz = imgPIL.getpixel((x,y))
        
        # công thức 6.7.1 trang 445 : tính euclidean distance
        d= np.sqrt((rz - ravg)**2   + (gz - gavg)**2 + (bz - bavg)**2)
        
        # so sánh giá trị ngưỡng
        if d <= nguong:
            # background
            seg.putpixel((x,y),(255,255,255))
        else :
            # object
            seg.putpixel((x,y),(bz, gz, rz))
                            
#chuyển ảnh từ pil sang opencv để hiển thị
imgseg = np.array(seg)

#cv2.imshow ('original image'    , img )    
cv2.imshow ('segmentation'         , imgseg )  

cv2.waitKey(0)
cv2.destroyAllWindows()  