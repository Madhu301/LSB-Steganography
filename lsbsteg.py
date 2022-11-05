import cv2  # To process images
import numpy as np

def data2binary(data):
    # convert data to binary
    if type(data)==str:
        return ''.join([format(ord(i),"08b") for i in data])
    #convert pixels of images to binary
    elif type(data)==bytes or type(data)==np.ndarray:      # pixels are passed as array
        return [format(i,"08b") for i in data]

def hidedata(image,data):
    #helps in decoding limit
    data+="#####"
    dataIndex=0
    # convert data to binary
    binaryData=data2binary(data)
    #length of data
    datalen=len(binaryData)
    # taking each pixel [R,G,B] from image 
    for values in image:
        for pixel in values:
            r,g,b=data2binary(pixel) #change each pixel to binary
            
            #hiding data in pixel
            if dataIndex<datalen:
                pixel[0]=int(r[:-1]+binaryData[dataIndex])
                dataIndex+=1
            
            if dataIndex<datalen:
                pixel[1]=int(g[:-1]+binaryData[dataIndex])
                dataIndex+=1
            
            if dataIndex<datalen:
                pixel[2]=int(b[:-1]+binaryData[dataIndex])
                dataIndex+=1

            if dataIndex>=datalen:
                break
    return image
def encode():
    # get image 
    imageName=input("Enter Image Name: ")

    # read R,G,B value (pixels) of the image and stores it in image
    image=cv2.imread(imageName) 

    # get message
    data=input("Enter the Message: ") 

    # checking validity of data
    if data==0:
        raise ValueError("Data is empty")    # throwing manual exception

    # name of steg image
    stegImg=input("Enter the desired encoded image Name: ")

    # pass image & data
    encodedData=hidedata(image,data)

    # creating steg image with encoded pixels
    cv2.imwrite(stegImg,encodedData)

def showdata(image):
    binaryData=""
    for values in image:
        for pixel in values:
            r,g,b=data2binary(pixel)

            #extracting the LSB bits of pixel [r,g,b]
            binaryData+=r[-1]
            binaryData+=g[-1]
            binaryData+=b[-1]
    
    #convertng binary data to bytes (separating 8 bits)
    allByte=[binaryData[i:i+8]for i in range(0,len(binaryData),8)]
    
    
    #converting to text
    decodedData=""
    for byte in allByte:
        decodedData+=chr(int(byte,2))
        if decodedData[-5:]=="#####":    # 5 # is the end of our data
            break
    
    return decodedData[:-5]

def decode():
    # get steg Image
    ImageName=input("Enter image name you want to extract from: ")
    image=cv2.imread(ImageName)

    text=showdata(image)
    return text

def steganography():
    operation=int(input("1.Encode  \n2.Decode \nEnter Here: "))

    if operation==1:
        encode()
    else:
        plaintext=decode()
        print("Decoded Message: ",plaintext)
 
steganography()