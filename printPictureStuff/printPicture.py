import numpy as np
from PIL import Image
import sys
from rich.console import Console
from rich import print
from rich.style import Style
from rich.panel import Panel
from rich.progress import Progress

removeLine = '\033[F'
moveUp = '\033[A'
moveDown = '\033[B'
clearScreen = '\033[2J'

console = Console()

def get_image(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error: {e}")
        return None

def resize_image(image, new_width):
    print()
    width_percent = (new_width / float(image.size[0]))
    new_height = int((float(image.size[1]) * float(width_percent)))
    resized_image = image.resize((int(new_width), int(new_height)), Image.NEAREST)
    return resized_image

# symbol that is used to represent two pixels above each other background is the higher pixel and foreground is the lower pixel
symbol = '▄'

def get_pixel_color(image:Image, x, y):
    r, g, b = image.getpixel((x, y))
    return r, g, b

class PixelImage():
    def __init__(self, image:Image):
        self.image = image
        self.pixel_array = np.array(image)
        self.width = self.pixel_array.shape[1]
        self.height = self.pixel_array.shape[0]
        if self.height % 2 != 0:
            # add a row of black pixels to make the height even at the bottom
            self.pixel_array = np.vstack((self.pixel_array, np.zeros((1, self.width, 3), dtype=np.uint8)))
            self.height += 1
        self.displayHeight = self.height / 2 # two pixels are represented by one symbol
        
    
    def get_pixel_color(self, x, y):
        r, g, b = self.image.getpixel((x, y))
        return r, g, b
    
    def get_symbol(self, x, y):
        upper_pixel = self.get_pixel_color(x, y)
        lower_pixel = self.get_pixel_color(x, y+1)
        return upper_pixel, lower_pixel
    
    def color_style(self, upper_pixel, lower_pixel):
        style = Style(bgcolor=upper_pixel, color=lower_pixel)
        return style
    
    
    def run(self):
        console = Console()
        #console.clear()
        console.log(Panel(f"Image size: [red]{self.width}[/]x{self.height}"))
        picture = np.zeros((self.height, self.width), dtype=object)
        with Progress() as progress:
            task1 = progress.add_task("[red]Rendering Picture...[/]", total=self.displayHeight)
            for y in range(0, self.height-2, 2):
                for x in range(self.width):
                    upper_pixel, lower_pixel = self.get_symbol(x, y)
                    #print('uper_pixel:', upper_pixel, '  lower_pixel:', lower_pixel)
                    #style = f'rgb{lower_pixel} on rgb{upper_pixel}]'
                    style = Style(color=f'rgb{lower_pixel}', bgcolor=f'rgb{upper_pixel}')
                    picture[y,x] = style
                    #console.print('['+style + symbol + '[/'+style)
                    #print(style + symbol + '[/]', end='')
                    #print(style, end='')
                    #console.print(symbol, style=style, end='')
                #console.print()
                #time.sleep(0.0001)
                progress.update(task1, advance=1)
        #pprint.pprint(picture)
        for y in range(0, self.height-2, 2):
            for x in range(self.width):
                #console.log(f"y: {y} x: {x} style: {picture[y][x]}")
                console.print(symbol, style=picture[y][x], end='')
            console.print()

def main():
    if len(sys.argv) > 1:
        image_paths = sys.argv[1:]
        for image_path in image_paths:
            image = get_image(image_path)
            if image:
                #print(np.array(image).shape)
                if image.height % 2 != 0:
                    # add a row of black pixels to make the height even at the bottom
                    image = Image.fromarray(np.vstack((image, np.zeros((1, image.width, 3), dtype=np.uint8))))
                #print(np.array(image).shape)
                new_width = (2*648)/image.height * image.width
                image = resize_image(image, new_width)
                pixel_image = PixelImage(image)
                pixel_image.run()
    else:
        image_path = 'bild.png'
        image = get_image(image_path)
        if image:
            new_width = 100
            image = resize_image(image, new_width)
            pixel_image = PixelImage(image)
            pixel_image.run()

with Console() as console:
    console.print("Hello, [rgb(5, 46, 52) on rgb(5, 255, 56)]World![/]")

if __name__ == '__main__':
    main()