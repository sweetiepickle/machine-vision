#Import Thư Viện
import cv2 as cv #Khai báo thư viện OpenCV
import numpy as np #Thư viện tính toán chuyên dụng dùng cho ma trận
from PIL import Image #Thư viện xử lý ảnh PILLOW hỗ trợ nhiều định dạng ảnh
import matplotlib.pyplot as plt #Thư viện để vẽ biểu đồ

#Khai báo đường dẫn filehinh
filehinh = r'astley.png'

#Đọc ảnh màu dùng thư viện OpenCV được mã hóa thành ma trận 3 chiều 
img = cv.imread(filehinh,cv.IMREAD_COLOR)

#Đọc ảnh màu PIL. Ảnh PIL sẽ dùng để thực hiện các tác vụ tính toán và xử lý
imgPIL = Image.open(filehinh)

#Lấy kích thước của ảnh từ imgPIL
width = imgPIL.size[0]
height = imgPIL.size[1]

#----------------------------------------------------------------------------------------

def ChuyenDoiAnhMauRGBSangAnhXamLuminance(imgPIL):
    luminance = Image.new(imgPIL.mode, imgPIL.size)
    
    #Lấy kích thước của ảnh từ imgPIL
    width = imgPIL.size[0]
    height = imgPIL.size[1]
    
    for x in range(width):
        for y in range(height):
            #Lấy giá trị điểm ảnh tại vị trí (x,y)
            R,G,B = imgPIL.getpixel((x,y))

            gray_luminance = np.uint8(0.2126*R+0.7152*G+0.0722*B)

            #Gán giá trị mức xám cho các ảnh
            luminance.putpixel((x,y),(gray_luminance,gray_luminance,gray_luminance))

    return luminance

def Gray_Image_Edge(imgGray, threshold):
    
    Edge_Detection_img = Image.new(imgGray.mode, imgGray.size)

    width = imgGray.size[0]
    height = imgGray.size[1]

    #Ma trận Sobel
    Sobel_matrix_x = [ [ -1, -2, -1 ], [ 0, 0, 0 ], [ 1, 2, 1 ] ]
    Sobel_matrix_y = [ [ -1, 0, 1 ] , [ -2, 0, 2 ], [ -1, 0, 1 ] ]

    for x in range(1,width-1):
        for y in range(1,height-1):

            #Khai báo 3 biến để chứa tổng Gradien x va y va bien cua vector
            Gradien_x = 0
            Gradien_y = 0
            Magnitude_V = 0


            for i in range(x-1,x+2):
                for j in range(y-1,y+2):
                    # Lấy điểm màu tại từng vị trí
                    R,G,B = imgGray.getpixel((i,j))

                    Gradien_x += R*Sobel_matrix_x[(abs(x-i-1))][(abs(y-j-1))]
                    Gradien_y += R*Sobel_matrix_y[(abs(x-i-1))][(abs(y-j-1))]

            Magnitude_V = abs(Gradien_x) + abs(Gradien_y)

            if(Magnitude_V<=threshold):
                Edge_Detection_img.putpixel((x,y),(np.uint8(0),np.uint8(0),np.uint8(0)))
            else:
                Edge_Detection_img.putpixel((x,y),(np.uint8(255),np.uint8(255),np.uint8(255)))

    return Edge_Detection_img


def create_mask(radius):
    # Chuẩn hóa kích thước size theo cthuc
    size = 2*radius + 1
    center = radius

    # Tạo ma trận nhị phân có kích thước size
    struct_elem = np.zeros((size, size), dtype=np.uint8)
    
    # Tạo list chứa ma trận nhị phân và số lượng giá trị nhị phân mức 1
    list = []
    a = 0
    
    # Set giá trị cho ma trận nhị phân
    for i in range(size):
        for j in range(size):
            if (i - center)**2 + (j - center)**2 <= radius**2:
                struct_elem[i, j] = 1
                a = a + 1
    list = [struct_elem, a]

    return list 

def Erode(img_input, radius):
    
    # Lưu trữ kết quả
    erosion_img = Image.new(img_input.mode, img_input.size)
    
    # Lấy kích thước
    img_width = img_input.size[0]
    img_height = img_input.size[1]
    
    # Tạo ma trận kernel
    list = create_mask(radius)
    number = list[1]
    
    for width in range(radius, img_width - radius): 
        for height in range(radius, img_height - radius):
            
            Rs = 0
            count = 0
            
            for i in range(width - radius, width + radius + 1): 
                for j in range(height - radius, height + radius + 1):
                    mask = list[0]

                    r, g, b = np.uint8(img_input.getpixel((i,j))) 
                    Rs = r * mask[i -  (width - radius), j - (height - radius)]
                    
                    #Erosion algorithm
                    if(Rs != 0):
                        count = count + 1
                        if(count == number):
                            erosion_img.putpixel((width, height), (Rs, Rs, Rs))
                        elif (count < number):
                            erosion_img.putpixel((width, height), (0, 0, 0))
    return erosion_img

def Dilate(img_input, radius):
    
    dilate_img = Image.new(img_input.mode, img_input.size)
    
    img_width = dilate_img.size[0]
    img_height = dilate_img.size[1]
    
    list = create_mask(radius)

    for width in range(radius, img_width - radius):
        for height in range(radius, img_height - radius):

            Rs = 0
            for i in range(width - radius, width + radius + 1):
                for j in range(height - radius, height + radius + 1):
                    mask = list[0]

                    r, g, b = np.uint8(img_input.getpixel((i,j))) 
                    
                    Rs = r * mask[i -  (width - radius), j - (height - radius)]
                    
                    #Dilation algorithm
                    if(Rs != 0):
                        dilate_img.putpixel((width, height), (Rs, Rs, Rs))          
    return dilate_img

# Giúp làm mượt các đường viền, phá vỡ các khe nhỏ, 
# loại bỏ các đối tượng nhỏ, làm mượt các đỉnh lồi.

def Opening(edimg, radius):     # dilation phép toán erosion
    opening_img_tem = Erode(edimg, radius)
    opening_img = Dilate(opening_img_tem, radius)
    return opening_img

# Giúp làm mượt các đường viền, loại bỏ các lỗ nhỏ, làm mượt các đỉnh khe hẹp.

def Closing(edimg, radius):     # erosion phép toán dilation
    closing_img_tem = Dilate(edimg, radius)
    closing_img = Erode(closing_img_tem, radius)
    return closing_img

#---------------------------------------------------------------------------------------

Anh_Xam = ChuyenDoiAnhMauRGBSangAnhXamLuminance(imgPIL)
Edge_Img = Gray_Image_Edge(Anh_Xam,60)

Erode_Img = Erode(Edge_Img,1)
Dilate_Img = Dilate(Edge_Img,1)

Open_Img = Opening(Edge_Img,1)
Close_Img = Closing(Edge_Img,1)

#Convert PIL_CV2
Anh_Xam = np.array(Anh_Xam)
Edge_Img = np.array(Edge_Img)

Erode_Img = np.array(Erode_Img)           
Dilate_Img = np.array(Dilate_Img)

Open_Img = np.array(Open_Img)
Close_Img = np.array(Close_Img)  

#Show Image
cv.imshow('Original Image', img)
cv.imshow('Luminance Image', Anh_Xam)
cv.imshow('Edge Image', Edge_Img)
cv.imshow('Erode Image', Erode_Img)
cv.imshow('Dilate Image', Dilate_Img)
cv.imshow('Open Image', Open_Img)
cv.imshow('Close Image', Close_Img)

#Bấm phím bất kì để đóng cửa sổ
cv.waitKey()

#Quit key
cv.destroyAllWindows()