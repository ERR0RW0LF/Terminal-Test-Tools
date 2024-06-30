import numpy as np
from PIL import Image
import sys
from rich.console import Console
from rich import print
from rich.style import Style

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
        
        self.pixel_array = np.array(self.image)
        
        self.width = self.pixel_array.shape[1]
        self.height = self.pixel_array.shape[0]
        
        # if the y acis is odd, then it will add a row of zeros to make it even
        if self.height % 2 != 0:
            # add a row of black pixels to make the height even at the bottom
            self.pixel_array = np.vstack((self.pixel_array, np.zeros((1, self.width, 3), dtype=np.uint8)))
            self.height += 1
        
        self.displayHeight = self.height / 2 # two pixels are represented by one symbol
        
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

def get_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error: {e}")
        return None


def resize_image(image:Image, new_width):
    width_percent = (new_width / float(np.array(image).shape[0]))
    new_height = int((float(np.array(image).shape[1]) * float(width_percent)))
    resized_image = np.array(image).resize((int(new_width), int(new_height)), Image.NEAREST)
    return resized_image
    

def main():
    console = Console()
    image_path = 'bild.png'
    image = get_image(image_path)
    if image:
        #print(np.array(image).shape)
        if image.height % 2 != 0:
            # add a row of black pixels to make the height even at the bottom
            image = Image.fromarray(np.vstack((image, np.zeros((1, image.width, 3), dtype=np.uint8))))
        #print(np.array(image).shape)
        new_width = (2*648)/image.height * image.width
        image = resize_image(image, new_width)
    testImage = renderPicture(image)
    print(testImage.image.shape)
    console.print(testImage.pictureToASCII())

if __name__ == '__main__':
    
    
    main()