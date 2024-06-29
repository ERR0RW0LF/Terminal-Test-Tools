from calendar import c
from turtle import width
from cv2 import resize
import numpy as np
from PIL import Image
from rich.console import Console

symbol = '▄'

class renderPicture():
    def __init__(self, image):
        # if the last three letters are png, jpg, jpeg, or bmp, then it will open the image
        if (image[-3:] == 'jpg' or image[-4:] == 'jpeg' or image[-3:] == 'bmp'):
            self.image = Image.open(image).convert('RGB')
        elif image[-3:] == 'png':
            self.image = Image.open(image).convert('RGB')
        else:
            exit('The file is not a valid image file. Please try again.')
        
        
        # if the y acis is odd, then it will add a row of zeros to make it even
        if self.image.size[1] % 2 != 0:
            self.addToPictureY(1)
        print(self.image.shape)
        
        self.resizePicture()

    def getPicture(self):
        return self.image

    def printPicture(self):
        img = Image.fromarray(self.image, 'RGB')
        img.show()

    def savePicture(self, path):
        img = Image.fromarray(self.image, 'RGB')
        img.save(path)

    def changePicture(self, image):
        self.image = image

    def changePixel(self, x, y, color):
        self.image[x][y] = color

    def changeRow(self, x, color):
        self.image[x] = color

    def changeColumn(self, y, color):
        self.image[:,y] = color

    def changeColor(self, color):
        self.image = color

    def changeSize(self, size):
        self.image = np.zeros((size[0], size[1], 3), dtype=np.uint8)
    
    def changeBaseColor(self, color='RGB'):
        self.image = self.image.astype(color)
    
    def addToPictureY(self, newYSize: int):
        self.image = np.concatenate((self.image, np.zeros((newYSize, np.array(self.image).shape[1], 3), dtype=np.uint8)), axis=0)
    
    def addToPictureX(self, newXSize: int):
        self.image = np.concatenate((self.image, np.zeros((np.array(self.image).shape[0], newXSize, 3), dtype=np.uint8)), axis=1)
    
    def addBorder(self, borderSize: int, color=(0,0,0)):
        self.image = np.pad(self.image, ((borderSize, borderSize), (borderSize, borderSize), (0,0)), mode='constant', constant_values=color)
    
    def addToPicture(self, x: int, y: int):
        self.addToPictureY(y)
        self.addToPictureX(x)
    
    def pictureShape(self):
        return self.image.shape
    
    def getPixel(self, x, y):
        return self.image[x][y]
    
    def getTwoPixels(self, x, y):
        return self.image[x][y], self.image[x][y+1]
    
    def pictureToASCII(self):
        ascii = ''
        for y in range(np.array(self.image).shape[1]):
            for x in range(np.array(self.image).shape[0]):
                colorOne, colorTwo = self.getTwoPixels(x, y)
                ascii += f'[rgb{colorOne} on rgb{colorTwo}]{symbol}[/]'
            ascii += '\n'
        return ascii
    
    def resize_image(self, new_width):
    widthPercent = (new_width / float(self.image.shape[0]))
    new_height = int((float(self.image.size[1]) * float(width_percent)))
    resized_image = self.image.resize((int(new_width), int(new_height)), Image.NEAREST)
    return resized_image
    
    def resizePicture(self):
        hight = self.image.shape[1]
        width = self.image.shape[0]
        newWidth = (648)/hight * width
        newHight = 648
        self.image = resize(self.image, (newWidth, newHight))


def main():
    console = Console()
    testImage = renderPicture('test.jpg')
    print(testImage.image.shape)
    console.print(testImage.pictureToASCII())

if __name__ == '__main__':
    
    
    main()