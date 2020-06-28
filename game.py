from board import Board
from termcolor import colored
import os
import random
os.system('color')
g = Board(8,8)
g.print_grid()
while (True):
    try:
        g.input_move()
    except ValueError:
        pass
    except KeyboardInterrupt:
        print("Good bye ...")
        break