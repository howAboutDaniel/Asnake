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
GREY = (128, 128, 128)      # gridlines
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

# heuristicka funkcia:
    # Manhattan Distance
    def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x2 - x1) + (y2 - y1)

    # Euclid Distance
    # TODO

# vytvorenie mriezky do okna
def do_grid(rows, width):
        grid = [] 
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows): # collumns, just called rows cos it's a square
                node = Node(i, j, gap, rows)
                grid[i].append(node)
        return grid

# gridlines only
def gridlines(win, rows, width):
    gap = width // rows
    for i in range(rows): # horizontal line
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):	# vertical line
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# function that actually draws everything
def draw(win, grid, rows, width): 
    win.fill(WHITE)
    
    # calling method draw(self, win) for all the nodes in the grid
    for row in grid:
      for node in row:
          node.draw(win)
    gridlines(win, rows, width) # draw gridlines
    pygame.display.update()
	

# Function that determines wich node to draw based on mouse position that will translate into x and y position
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


# event setup
def main(win, width):
	ROWS = 50 # code to work with user input
	grid = do_grid(ROWS, width) 

	start = None # start position
	end = None # end position

	run = True
    # loop throu all the events that had happend and figure out what they're doing
	while run:
    # while loop runs while the algorithm runs but when the algo started, user isn't able to change anything anymore as in not to mess up the process
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

            # checking the mouse position and if the left button's been pressed
			if pygame.mouse.get_pressed()[0]: # LEFT BUTTON
				pos = pygame.mouse.get_pos() # x, y coordinates
				row, col = get_clicked_pos(pos, ROWS, width) # what actual node did we click on
				node = grid[row][col] # indexing row and col in the grid
                
				# doing the start position first, if the start node isn't in the grid, do them next
				if not start and node != end: # condition that ensures that the start node won't be drawn over end node
					start = node 
					start.do_start()
                
				# doing the end position second, if the end node isn't in the grid, do them next
				elif not end and node != start: # condition that ensures that the end node won't be drawn over start node
					end = node
					end.do_end()
				
				# when not clicking on the start or the end, then make it a wall
				elif node != end and node != start:
					node.do_wall()
			# a condition that checks whetter a right button's been pressed and if so, reset the node's colour to the white
			elif pygame.mouse.get_pressed()[2]: # RIGHT BUTTON
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				node = grid[row][col]
				node.do_restart()
				if node == start:
					start = None
				elif node == end:
					end = None

	pygame.quit()

main(WIN, WIDTH)
