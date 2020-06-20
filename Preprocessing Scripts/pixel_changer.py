import os
import cv2
from PIL import Image

def main():
    for num, imgf in enumerate(sorted(os.listdir("masks"))):
        imgf = "masks/" + imgf 
        img = Image.open(imgf)
        print(img)
        pixels = img.load()

        im = Image.new( img.mode, img.size)
        pixelsNew = im.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                if pixels[i,j] == (255,0,0):
                    pixelsNew[i,j] = (1,1,1)
                else:
                    pixelsNew[i,j] = (0,0,0)
        im.save(imgf)
 
if __name__ == '__main__': 
      
    main()        