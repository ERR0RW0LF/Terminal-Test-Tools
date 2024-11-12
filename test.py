from rich.console import Console
from rich import print

removeLine = '\033[F'
moveUp = '\033[A'
moveDown = '\033[B'
clearScreen = '\033[2J'

console = Console()
string = "Error: err0rw0lf was detected!"
if len(string) % 2 != 0:
    x = ((len(string)-1)/2)
    console.print("\n"*int(x))
else:
    x = len(string)/2
    console.print("\n"*int(x))

console.log(string, style="green")
if len(string) % 2 != 0:
    x = ((len(string)-1)/2)
    console.print("\n"*int(x))
else:
    x = len(string)/2
    console.print("\n"*int(x))
