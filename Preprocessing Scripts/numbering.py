import os

def main():
    for i, img in enumerate(sorted(os.listdir("images"))):
        dst = "images/" + str(i) + ".png"
        src = "images/" + img
        os.rename(src, dst)

if __name__ == '__main__': 
       
    main() 