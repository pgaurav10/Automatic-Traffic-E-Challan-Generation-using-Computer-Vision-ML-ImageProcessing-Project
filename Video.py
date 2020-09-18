import cv2 
import os 
from PIL import Image

def GenerateFrames():
    cam = cv2.VideoCapture("opencv.mp4") 
    
    fps = int(cam.get(cv2.CAP_PROP_FPS))  
    print(fps)
    try: 
        if not os.path.exists('data'): 
            os.makedirs('data') 
    
    except OSError: 
        print ('Error: Creating directory of data') 
    
      
    ret = True 
    
    currentframe = 0 
    while(ret): 
        ret,frame = cam.read()
        if currentframe%(1*fps) == 0:
            name = './data/frame' + str(currentframe) + '.jpg' 
            print ('Creating...' + name)
            cv2.imwrite(name, frame) 
        currentframe += 1 
           
    cam.release() 
    cv2.destroyAllWindows()
    
    imageObject = Image.open("./data/frame368.jpg")

    cropped = imageObject.crop((1000,1480,3400,2150))
    cropped.save('Cropped.png','PNG') 
    #cropped.show()
    
    size = 1280, 670
    im = Image.open("Cropped.png")
    im_resized = im.resize(size, Image.ANTIALIAS)
    im_resized.save("Test.png", "PNG")


