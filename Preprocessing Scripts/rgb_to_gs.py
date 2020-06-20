import os
import cv2

def main():
    for i, imgf in enumerate(sorted(os.listdir("masks"))):
        imgf = "masks/" + imgf
        img = cv2.imread(imgf, 1)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(imgf, img_gray)
    

if __name__ == '__main__': 
    
    main() 