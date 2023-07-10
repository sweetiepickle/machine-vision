# Lê Bảo Khương - 20146123

import cv2          #opencv để xử lí ảnh
import numpy as np  #tính toán ma trận

#dùng opencv đọc ảnh màu và trả lại 1 ma trận pixel
img =   cv2.imread('astley.png'  , cv2.IMREAD_COLOR)            #imread : đọc ảnh , thông số đọc là color ( đọc ảnh màu )   
code =  cv2.imread('code.png'    , cv2.IMREAD_COLOR)

#lấy kích thước ảnh
h = len (img[0])
w = len (img[1])

#khai báo biến chứa hình ở 3 kênh màu
red     = np.zeros ((w,h,3) , np.uint8)         #số 3 là 3 kênh r, g, b, mỗi kênh 8bit
green   = np.zeros ((w,h,3) , np.uint8) 
blue    = np.zeros ((w,h,3) , np.uint8)   

#set zero cho tất cả điểm ảnh có trong 3 kênh lúc đầu
red     [:] = [0,0,0]
green   [:] = [0,0,0]
blue    [:] = [0,0,0]

#2 vòng for đọc giá trị mỗi pixel
for x in range (w):
    for y in range (h):
        
        #lấy giá trị điểm ảnh tại tọa độ (x,y)
        R = img [x,y,2]         #layer thứ 2
        G = img [x,y,1]         #layer thứ 1
        B = img [x,y,0]         #layer thứ 0
        
        #thiết lập màu cho các kênh
        red     [x,y,2] = R
        green   [x,y,1] = G
        blue    [x,y,0] = B 
        


# display image as a new window
cv2.imshow ('original image'    , img)
cv2.imshow ('red channel'       , red)
cv2.imshow ('green channel'     , green)
cv2.imshow ('blue channel'      , blue)
#cv2.imshow ('code'              , code)

#esc = phím bất kì
cv2.waitKey (0)

#giải phóng bộ nhớ dùng để hiển thị hình
cv2.destroyAllWindows() 


