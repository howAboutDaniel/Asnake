# required modules
import pygame
import math
from queue import PriorityQueue

# initializing the window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH)) 				# stvorcovy rozmer
pygame.display.set_caption("A* Snake Hunting It's Prey") 	# banner

# declaration of colors
RED = (255, 0, 0)			#      
GREEN = (0, 255, 0)			#        
WHITE = (255, 255, 255)     # empty space
BLACK = (0, 0, 0)           # wall / barrier
PURPLE = (128, 0, 128)      # reconstructed path
ORANGE = (255, 165 ,0)      # start node
GREY = (128, 128, 128)      # gridlines
TURQUOISE = (66, 222, 2010) # end node/the prey

class Node:
	# initializing variables of the nodes
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width 
        self.x = row * width    # x coordinate
        self.y = col * width    # y coordinate
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    # passes on the position of the nodes
    def get_pos(self):
        return self.row, self.col
    
	# passes on an iformation about the color of the nodes
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
    
    # Adjusting node color based on the state
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

    # Recoloring the node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    # Check every direction along the way - down, up, right, left  
    # Function in order to see if nodes are walls or not
    # If they are not walls add them to the neighbors list
    
    def update_neighbors(self, grid):
        self.neighbors = []
        
        # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # Look DOWN
        # Current row position is less than the total of the rows minus 1 AND there's no a wall
        # Add the lower neighbor to the queue
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].wall_node(): 
            self.neighbors.append(grid[self.row + 1][self.col])
        
		# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # Look UP
        # Row position is not 0 AND there's no wall in this direction
        # Add the upper neighbor to the queue
        if self.row > 0 and not grid[self.row - 1][self.col].wall_node():
            self.neighbors.append(grid[self.row - 1][self.col])
        
		# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # Look RIGHT
        # Horizontal movement is analogic to the vertical
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].wall_node():
            self.neighbors.append(grid[self.row][self.col + 1])
		
        # ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
        # Look LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].wall_node():
             self.neighbors.append(grid[self.row][self.col - 1])

    # less than metoda, ktora vzdy vyhodnoti ze kazdy aktualny uzol je mensi nez susedny uzol
    def __lt__(self, other):
        return False

# Heuristic - Manhattan Distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + (y2 - y1)

'''
# End to Start point path plot function

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.do_path()
		draw()

# Raw A*

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue() # Module imported from queue
     
    # API for priority queue, adding start node with it's original f score into the open set
    # count's purpose is to keep track of when an item was inserted into the queue
    # the reason for that is to break ties if there are two (or more) items in the queue with the same f score
    # From those items with the same f score, program will pick the item that has entered the queue first
	open_set.put((0, count, start))
    
    # From where has this node node came from
	came_from = {}
    
    # distance from the start node to the current node
	g_val = {node: float("inf") for row in grid for node in row}
	g_val[start] = 0
    
	f_val = {node: float("inf") for row in grid for node in row}
	f_val[start] = h(start.get_pos(), end.get_pos())

     # Priority queue hasn't got anything to tell us if the node is in the queue or not and we need to check if there's something in the queue or not
     # Keeps track of what is in the priority queue and what isn't
	open_set_hash = {start}

     # Algo runs until the set is empty, if the open set is empty then every node has been considered and if we've not found a path, path doesn't exist
	while not open_set.empty():
		# Precausion for while loop in case it takes over, exit strategy
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

        # open_set stores f_val, count and node
        # We're only after the node, hence the index 2
		current = open_set.get()[2]
          
        # Taking whichever node popped out of the priority queue and sync it with open_set_hash by removing it form it to avoid duplicates
		open_set_hash.remove(current)

        # condition that checks wether the node we're currently at is the end node, do a reconstruction of the path
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

        # consider all of the neighbors of the current node
		for neighbor in current.neighbors:
			
			# all of the edges have width of 1 and what we're doing here is
            # if we wanna figure out what the temporary g_val of this neighbor would be assuming we go to this neighbor from whatever node we're at
            # then we take the currently known shortest distance and add 1 to it because we're moving one node over to the best-fit neighbor
			temp_g_val = g_val[current] + 1

            # this conditions check for a better way to reach it's neighbor. if there's one, it will get updated
			if temp_g_val < g_val[neighbor]:
				came_from[neighbor] = current
				g_val[neighbor] = temp_g_val
				f_val[neighbor] = temp_g_val + h(neighbor.get_pos(), end.get_pos())
                    
                # checking if the neighbor is in the open set or not
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_val[neighbor], count, neighbor)) # better path then found before
					open_set_hash.add(neighbor)
					neighbor.do_open()

		draw()

        # condition that checks for a case when the current node we're at is not a start node. In such case, close it off and make it red
		if current != start:
			current.do_closed()

    # path not found case
	return False
    '''

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


# Event setup
def main(win, width):
	ROWS = 50
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
'''
			# start running algorithm after the first two lines of code, being initial conditions.
			# First thing that needs to be squared away, will be rulling out unreachable node states (or neighbors in this case). Meaning areas within enclosed walls. 

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for node in row:
							node.update_neighbors(grid) # whenever the space key is pressed call method update_neighbors

                    # once we start, we're gonna call a draw function so we can pass a return value of that draw function as an argument to the A* algorithm function
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
				
                # when C key is pressed, to this
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = do_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)
'''