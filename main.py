# potrebne moduly
import pygame
import math
from queue import PriorityQueue

# nastavenie velkosti okna
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) # stvorcovy rozmer
pygame.display.set_caption("A* Snake Hunting It's Prey")

# deklaracia farieb
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)     # prazdny priestor
BLACK = (0, 0, 0)           # steny/prekazky
PURPLE = (128, 0, 128)      # cesta
ORANGE = (255, 165 ,0)      # start
GREY = (128, 128, 128)
TURQUOISE = (66, 222, 2010) # konec/korist

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width 
        self.x = row * width    # suradnica x
        self.y = col * width    # suradnica y
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    # metody ktore programu hovoria v akom stave sa dany uzol nachadza
    def get_pos(self):
        return self.row, self.col
    
    def open_list(self):
        return self.color == GREEN
    
    def closed_list(self):
        return self.color == RED
    
    def wall_node(self):
        return self.color == BLACK
    
    def start_node(self):
        return self.color == ORANGE
    
    def end_node(self):
        return self.color == TURQUOISE
    
    # metody ktore prefarbuju uzly na zaklade ich stavu/funckie
    def do_start(self):
        self.color = ORANGE
    
    def do_restart(self):
        self.color = WHITE
    
    def do_open(self):
        self.color = GREEN
    
    def do_closed(self):
        self.color = RED

    def do_wall(self):
        self.color = BLACK

    def do_end(self):
        self.color = TURQUOISE

    def do_path(self):
        self.color = PURPLE

    # metoda na vyfarbenie uzlov
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    # less than metoda, ktora vzdy vyhodnoti ze kazdy aktualny uzol je mensi nez susedny uzol
    def __lt__(self, other):
        return False