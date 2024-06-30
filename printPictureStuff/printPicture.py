import numpy as np
from PIL import Image
import sys
from rich.console import Console
from rich import print
from rich.style import Style

removeLine = '\033[F'
moveUp = '\033[A'
moveDown = '\033[B'
clearScreen = '\033[2J'

console = Console()