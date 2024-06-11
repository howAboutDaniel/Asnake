# Required modules
import pygame
import math
from queue import PriorityQueue

# Initializing the window
WIDTH = 800
# Square dimension
WIN = pygame.display.set_mode((WIDTH, WIDTH))
# Banner
pygame.display.set_caption("A* Path Finding Algorithm")

# Colours declaration
RED = (255, 0, 0)			# OPEN list
GREEN = (0, 255, 0)			# CLOSED list
WHITE = (255, 255, 255)		# Empty node
BLACK = (0, 0, 0)			# Wall / Barrier
PURPLE = (128, 0, 128)		# Reconstructed path
ORANGE = (255, 165 ,0)		# Start node
GREY = (128, 128, 128)		# Gridlines
TURQUOISE = (64, 224, 208) 	# End node / The prey

class Spot:
	# Node's initial variables
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width    # x coordinate
		self.y = col * width    # y coordinate
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	# Node's position is passed
	def get_pos(self):
		return self.row, self.col

	# Information about the node's colour is passed
	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE
	
	# Node color adjustment based on the node's state
	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

    # Drawing the node
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Check for a direction with a lowest cost
	def update_neighbors(self, grid):
		self.neighbors = []
		# Look DOWN
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])
		# Look UP
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])
        # Look RIGHT
		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])
        # Look LEFT
		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

# Heuristic - Manhattan Distance
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# End to Start point path plot function
def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# A*
def algorithm(draw, grid, start, end):
	count = 0
    # Queue module
	open_set = PriorityQueue()
	# Pick an item that has entered the queue first
	open_set.put((0, count, start))
    # From where has this node came from
	came_from = {}
    # Distance from the start node to the current node
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
    # Cost function
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())
    # Keeps track of what is in the queue
	open_set_hash = {start}
	
	# Algorithm runs until the set is empty
	while not open_set.empty():
		# Infinite loop precausion – exit strategy
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
        
		# open_set stores [f_val, count, node]
        # Node's index = 2
		current = open_set.get()[2]
		# Syncing nodes fromt the queue with open_set_hash to avoid duplicates
		open_set_hash.remove(current)
        
		# Condition that checks the end node status
		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

        # Consider all of the neighbors of the current node
		for neighbor in current.neighbors:
			# Searching neighbor nodes
			temp_g_score = g_score[current] + 1
			# If there's a better way to reach the neighbor
			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                # Checking if the neighbor is in the open set or not				
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

        # Case when the current node is not a start node
		# In such case, close it off and make it red
		if current != start:
			current.make_closed()

	# Case in wich the path is not found
	return False

# Creating grid in the main window
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows): # collumns, just called rows because it's a square
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)
	return grid

# Creating gridlines only
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Function that actually draws everything
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

# Function that determines which node to draw based on mouse position 
# That will get translated into x and y position
def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

# Event setup
def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)
	# start position
	start = None
	# end position
	end = None

	run = True

	# Looping through all the events that happend and selects appropriate action
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# Checking the position where the mouse had clicked and if it was the left one [0]
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				# If there's no start node (ORANGE) draw it with the next click
				# Condition that ensures that the start node won't be drawn over by the end node
				if not start and spot != end:
					start = spot
					start.make_start()

				# If there's no end node (TURQUOISE) draw it with the next click
                # Condition that ensures that the end node won't be drawn over by the start node
				elif not end and spot != start:
					end = spot
					end.make_end()

				# Drawing a wall when the start and the end node have already been drawed
				elif spot != end and spot != start:
					spot.make_barrier()
			
			# Checking the position where the mouse had clicked and if it was the right one [2]          
			# Reset the node's colour to the white
			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None
			
			# Start the algorithm after the initial conditions – first two lines
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid) # Whenever the space key is pressed call method update_neighbors

					# Draw function will be used as an argument for the algorithm visualization
					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				# When C key is pressed, clear everything
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)