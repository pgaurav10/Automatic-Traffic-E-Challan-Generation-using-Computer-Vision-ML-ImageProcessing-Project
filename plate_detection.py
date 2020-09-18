
import numpy as np
import cv2
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

vnumber = []
def cleanPlate(plate_img):
    gray= cv2.cvtColor(plate_img,cv2.COLOR_BGR2GRAY)
    ret1, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    cv2.imwrite("temp.png",thresh)
    image = cv2.imread('temp.png', cv2.IMREAD_GRAYSCALE)
    ret,thresh = cv2.threshold(image,220,255,cv2.THRESH_BINARY) 
    ret1,thresh1 = cv2.threshold(image,220,255,cv2.THRESH_BINARY) 
    gaus = cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,115,1)
    ret2,otsu = cv2.threshold(image,220,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    #cv2.imshow('Thresh',thresh);
    #cv2.imshow('Thresh1',thresh1);
    #cv2.imshow('Gaussian',gaus);
    #cv2.imshow('Otsu',otsu);
    #cv2.waitKey(0)

    ret, labels1 = cv2.connectedComponents(gaus)
    # Map component labels to hue val
    label_hue = np.uint8(179*labels1/np.max(labels1))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    
    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    
    # set bg label to black
    labeled_img[label_hue==0] = 255
    labeled_img[label_hue!=0] = 0
    
    labeled_img = cv2.resize(labeled_img, (0,0), fx=2, fy=2)
    gray_img = cv2.cvtColor(labeled_img, cv2.COLOR_BGR2GRAY)
    ret,lthresh = cv2.threshold(gray_img,220,255,cv2.THRESH_BINARY) 
    
    _,cnts,hierarchy= cv2.findContours(lthresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    list_rect = list()
    cntts = 0
    for c in cnts:
        #area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        rect_area = w*h
        if(rect_area > 1000 and rect_area < 9999):
            cv2.rectangle(labeled_img,(x,y),(x+w,y+h),255,1)
            list_rect.append([x,y,w,h])
            cntts = cntts +1
                    
    ht , wt , c = labeled_img.shape
    count = 0;
    if cntts < 15 and cntts > 6:
        for x in range(0,wt):
            for y in range(0,ht):
                for item in list_rect:
                    if not (x in range(item[0],item[0]+item[2]+1) and y in range(item[1],item[1]+item[3]+1)):
                        count = count + 1
                if count==len(list_rect):
                    labeled_img[y,x] = [0,0,0]
                count = 0
        
        for x in range(0,wt):
            for y in range(0,ht):
                if labeled_img[y,x].all() == 0:
                    labeled_img[y,x] = [255,255,255]
                else:
                   labeled_img[y,x] = [0,0,0] 
        labeled_img = cv2.resize(labeled_img, (0,0), fx=0.5, fy=0.5)
        
        plate_im = Image.fromarray(labeled_img)
        text = pytesseract.image_to_string(plate_im, lang='eng')
        print ("Detected Text : ",text)
        
        vnumber.append(text)
        return vnumber



def ratioCheck(area,width,height):
    ratio = float(width) / float(height)
    if ratio < 1:
        ratio = 1 / ratio
    aspect = 4.7272
    min = 30*aspect*30
    max = 80*aspect*80
    
    rmin = 2
    rmax = 8
    
    if(area < min or area > max) or (ratio < rmin or ratio > rmax):
        return False
    return True

def validate(min_rect):
    (x,y) , (width,height) , rect_angle = min_rect
    
    if width > height:
         angle = - rect_angle
    else:
        angle = 90 + rect_angle
        
    if angle > 15:
        return False
    if height == 0 or width == 0:
        return False
    
    area = height*width
    if not ratioCheck(area,width,height):
        return False
    else:
        return True




def GetNumber():
    img = cv2.imread("Test.png")
    
    blur_image = cv2.GaussianBlur(img, (5,5), 0)
    gray = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
    sobel = cv2.Sobel(gray,cv2.CV_8U,1,0,ksize=1)
    ret2,threshold_img = cv2.threshold(sobel,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
    element = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(31, 5))
    morph_img_threshold = threshold_img.copy()
    cv2.morphologyEx(src=threshold_img, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img_threshold)
    im2,contours, hierarchy= cv2.findContours(morph_img_threshold,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_SIMPLE)
    
    
    for cnt in contours:
        min_rect = cv2.minAreaRect(cnt)
        if validate(min_rect):
            x,y,w,h = cv2.boundingRect(cnt)
            plate_img = img[y:y+h,x:x+w]
            cv2.rectangle(img,(x,y),(x+w,y+h),255,0)
            hsv = cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV)
            plate_img = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
            
            new_text = cleanPlate(plate_img)
    
    return new_text