# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận
from PIL import Image
import math

#----------------------------------------------------------------------------------------------------------------------------------------------
# các hàm con
# def < tên hàm con > ( thông tin input )

def shp(imgPIL):
        
    # tạo 1 khung ảnh để chứa bitmap sau khi làm mượt
    sharp= Image.new(imgPIL.mode, imgPIL.size)
    
    # tạo ma trận thay thế hệ số c = -1 
    alterMatrix= np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
        
    # lấy kích thước ảnh
    w= imgPIL.size[0] 
    h= imgPIL.size[1]   
    
    # nhân ma trận thay thế thay vì tính laplacian
    for x in range (1,w-1): 
        for y in range (1,h-1):
            
            rs= 0
            gs= 0
            bs= 0
            
            sr= 0
            sg= 0
            sb= 0
            
            # quét các điểm trong mặt nạ
            for i in range (x-1,x+2):
                for j in range (y-1,y+2):
                    
                    # giá trị điểm ảnh tại từng pixel
                    R , G , B = imgPIL.getpixel((i,j))
                    
                    # cộng dồn giá trị
                    rs+= R*alterMatrix[i-x+1,j-y+1]
                    gs+= G*alterMatrix[i-x+1,j-y+1]
                    bs+= B*alterMatrix[i-x+1,j-y+1]
                    
            # tính f(x,y)
            R1, G1, B1= imgPIL.getpixel((x,y))        
            
            sr= R1 + rs
            sg= G1 + gs
            sb= B1 + bs

            if (sr<0):
                sr= 0
            elif (sr> 255):
                sr= 255
                
            if (sg<0):
                sg= 0
            elif (sg> 255):
                sg= 255
                
            if (sb<0):
                sb= 0
            elif (sb> 255):
                sb= 255
            
            sharp.putpixel((x,y),(sb,sg,sr))
            
    return sharp

#----------------------------------------------------------------------------------------------------------------------------------------------
# main

# mở file hình = đường dẫn
#filehinh= r'astley.png'
filehinh= r'bird_small.jpg'
img= cv2.imread(filehinh,cv2.IMREAD_COLOR) 

# đọc ảnh = pillow
imgPIL= Image.open(filehinh)

# làm sắc nét ảnh
shp3= shp(imgPIL)   

# chuyển ảnh từ pillow -> opencv
shp3cv= np.array(shp3)

cv2.imshow('Original',img)
cv2.imshow('3x3',shp3cv)

#----------------------------------------------------------------------------------------------------------------------------------------------
#esc = phím bất kì
cv2.waitKey (0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 
