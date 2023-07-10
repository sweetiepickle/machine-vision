import cv2              # Sử dụng thư viện xử lý ảnh openCV
from PIL import Image   # Sử dụng thư viện xử lý ảnh PILLOW hỗ trợ nhiều định dạng ảnh khác nhau
import numpy as np      # Sử dụng thư viện toán học, đặc biệt là các tính toán ma trận 
import math
imgPIL = Image.open(r'astley.png')
#______________________________________________________Convert RGB to Gray ___________________________________________________________

def TransRGBtoGrayusingAverage(imgPIL):
    # Copy the mode and size of the image
    grayscale_average           = Image.new(imgPIL.mode, imgPIL.size)
    width, height               = grayscale_average.size
    # Create an empty numpy array to store the grayscale values
    gray_image                  = np.empty((height, width), dtype=np.uint8)
    for x in range(width):
        for y in range(height):
            # Get the RGB values at position (x, y)
            R, G, B             = imgPIL.getpixel((x, y))
            # Calculate the average grayscale value
            gray_trans_average  = np.uint8((R + G + B) / 3)
            # Set the grayscale value in the numpy array
            gray_image[y, x]    = gray_trans_average    
    return gray_image

# ___________________________________________________  Haar Wavelet ___________________________________________________

def haar_wavelet(data):
    row         = data.shape[0] 
    coloumn     = data.shape[1] 
    rowplus     = np.zeros((row,int(coloumn/2)))
    rowminute   = np.zeros((row,int(coloumn/2)))
# ___________________________________________________haar wavelet transform  ( row transform )_______________________________________________-
 
    for j in range(0, row): # row 
        for i in range(0,coloumn,2): # coloumn 
            rowplus[j][int(i/2)]    = (data[j][i] + data[j][i+1])/math.sqrt(2) # row h0 
            rowminute[j][int(i/2)]  = (data[j][i] - data[j][i+1])/math.sqrt(2) # row h1 
            # string
    transform_row = np.zeros((row,coloumn))
# ___________________________________________________ Combine rowplus with rowminus  ___________________________________________________
 
    for k in range(0 , row):
        transform_row[k]        = np.concatenate((rowplus[k].astype(int),rowminute[k].astype(int)))

#  ___________________________________________________haar wavelet transform  ( column transform ) ___________________________________________________
 
    columnplus_h0                        = np.zeros((int(row/2),int(coloumn/2)))
    columnminute_h0                      = np.zeros((int(row/2),int(coloumn/2)))
    for j in range(0, int(coloumn/2)): # coloumn 
        for i in range(0,row,2): # row 
            columnplus_h0[int(i/2)][j]   = (rowplus[i][j] + rowplus[i+1][j])/math.sqrt(2) # a(m,n) approximation
            columnminute_h0[int(i/2)][j] = (rowplus[i][j] - rowplus[i+1][j])/math.sqrt(2) # dV(m,n) vertical detail 
    transform_column_h0 = np.zeros((row,int(coloumn/2)))
    
# ___________________________________________________ Combine columnplus_h0 with columnminute_h0  ___________________________________________________

    transform_column_h0         = np.concatenate((columnplus_h0,columnminute_h0))

#_______________________________-   Combine columnplus with columnminute    __________________________--  
    columnplus_h1                        = np.zeros((int(row/2),int(coloumn/2)))
    columnminute_h1                      = np.zeros((int(row/2),int(coloumn/2)))  
    for j in range(0, int(coloumn/2)): # coloumn 
        for i in range(0,row,2): # row 
            columnplus_h1[int(i/2)][j]   = (rowminute[i][j] + rowminute[i+1][j])/math.sqrt(2) #dH(m,n) horizontal detail  
            columnminute_h1[int(i/2)][j] = (rowminute[i][j] - rowminute[i+1][j])/math.sqrt(2) #dD(m,n)  diagonal detail
    transform_column_h1 = np.zeros((row,int(coloumn/2)))
# ___________________________________________________ Combine columnplus_h1 with columnminute_h1  ___________________________________________________

    transform_column_h1      = np.concatenate((columnplus_h1,columnminute_h1))

    return transform_column_h0 , transform_column_h1   # result of haar transformation

# ___________________________________________________ Processing  ___________________________________________________
#matran = [[100,50,60,150],  [75,105,][25,..]
#          [20,60,40,30],    [40 .. ,] [..,..
#          [50,90,70,82], 
#          [74,66,90,58]]

Gray_Image = np.array((TransRGBtoGrayusingAverage(imgPIL)))
# gray_array = Gray_Image[:, :, np.newaxis]  # Add a new axis to make it a 2D array

# ___________________________________________________ Show Image  ___________________________________________________

cv2.imshow('grayscale image',Gray_Image)
cv2.imshow('approximation & vertical',haar_wavelet(Gray_Image)[0])
cv2.imshow('horizontal & diagonal',haar_wavelet(Gray_Image)[1])

# Bấm phím bất kỳ để đóng cửa sổ hiển thị hình
cv2.waitKey(0)  
#Giải phóng bộ nhớ đã cấp phát cho các cửa sổ hiển thị hình 
cv2.destroyAllWindows()