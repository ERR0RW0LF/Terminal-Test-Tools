import numpy as np
from PIL import Image

class renderPicture():
    def __init__(self, image):
        # if the last three letters are png, jpg, jpeg, or bmp, then it will open the image
        if (image[-3:] == 'jpg' or image[-4:] == 'jpeg' or image[-3:] == 'bmp'):
            self.image = np.array(Image.open(image))
        elif image[-3:] == 'png':
            self.image = self.image[:,:,:3]
        else:
            exit('The file is not a valid image file. Please try again.')
        
        self.image = image

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
        self.image = np.concatenate((self.image, np.zeros((newYSize, self.image.shape[1], 3), dtype=np.uint8)), axis=0)
    
    def addToPictureX(self, newXSize: int):
        self.image = np.concatenate((self.image, np.zeros((self.image.shape[0], newXSize, 3), dtype=np.uint8)), axis=1)
    
    def addBorder(self, borderSize: int, color=(0,0,0)):
        self.image = np.pad(self.image, ((borderSize, borderSize), (borderSize, borderSize), (0,0)), mode='constant', constant_values=color)
    
    def addToPicture(self, x: int, y: int):
        self.addToPictureY(y)
        self.addToPictureX(x)
    
    