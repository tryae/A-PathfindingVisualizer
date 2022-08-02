from math import sqrt
import pygame

#set diagonals to flase to start with
diagonals = False

#the columns and rows for the grid
COLUMNS = 80
ROWS = 40

#width of screen and width of blocks
S_WIDTH = 1280
WIDTH = 16

#COLORS
LIGHTBLUE = (159, 197, 232)
DARKBLUE = (11, 83, 148)
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (119, 30, 202)

#CREATE WIN AND SET CAPTION
win = pygame.display.set_mode((1280,640))
pygame.display.set_caption('A* Path Finding Algorithm (no diagonals)')

#CREATE THE NODE TO BE USED FOR THE ALGORITHM
class Node:
	def __init__(self, row, col): 
		#set the row and col it is in to the node, once created they will not change
		self.row = row
		self.col = col
		#weather or it has already or will ever be evaluated when the A* algo runs
		self. walkable = True
		#default color
		self.color = WHITE
		#the .x and .y in pixels for where to draw the node
		self.x = col * WIDTH
		self.y = row * WIDTH

	def get_pos(self):
		return self.col, self.row

	#reset the values to the node
	def reset(self):
		self.color = WHITE
		self.walkable = True

	#change to the node to look and act like it is in the open list
	def make_open(self):
		self.color = DARKBLUE
		self.walkable = False

	#change the node to be in the closed list and change the waalkable value
	def make_closed(self):
		self.color = LIGHTBLUE
		self.walkable = False

	#make barrier
	def make_barrier(self):
		self.color = BLACK
		#can't be used by the algo
		self.walkable = False

	#create the starting node
	def make_start(self):
		self.color = RED
		self.walkable = False
	
	#create the end node
	def make_end(self):
		self.color = GREEN
		self.walkable = True

	#makes the node apart of the path that connects start and end
	def make_path(self):
		self.color = PURPLE

	#func for drawing it to the grid
	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, WIDTH, WIDTH))

#making the grid
grid = []
#creating the rows first
for i in range(ROWS):
	grid.append([])
	#making the columns second
	# this makes all the columns in the row then when it loops back make all the columns for the row after that
	for j in range(COLUMNS):
		node = Node(i, j)
		grid[i].append(node)

#makes the lines on the grid
def draw_grid():
	for i in range(ROWS):
		#draws it on win and sets the color. The next two are where it will be drawn and the last is the width the line will have.
		pygame.draw.line(win, BLACK, (0, i * WIDTH), (S_WIDTH, i * WIDTH), 2)
		for j in range(1, COLUMNS):
			pygame.draw.line(win, BLACK, (j * WIDTH, 0), (j * WIDTH, S_WIDTH),2)

#loops through all and draws the nodes and the grid
def draw():
	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid()
	pygame.display.update()

#get the cords of what node was clicked on
def get_clicked_pos(pos):
	y, x = pos
	row = y // WIDTH
	col = x //WIDTH
	return col, row 

# the shortest distance between the two Nodes
def manhattanH(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def Astar(start, end):
	#setting the start nodes values
	start.f = start.g = start.parent = 0
	#making the open and closed list
	openlist = []
	closedlist = []
	# appending start to the list 
	openlist.append(start)
	
	while openlist:
		current_node = openlist[0]
		current_index = 0

		#find the lowest f in the open list
		for index,i in enumerate(openlist):
			if i.f < current_node.f:
				# make it the current node and keep the index
				current_node = i
				current_index = index

		# if the current node is the end node make the path
		if current_node == end:
			while current_node.parent:
				# color parent node
				current_node.parent.make_path()
				# make parent node the current node
				current_node = current_node.parent
				# this draw makes it so it doesn't play instantly because the holy draw would be in the main func
				draw()
			# the start will be changed to path so this changes it back 
			current_node.make_start()
			return

		#if not end get the position of the current node
		col, row = current_node.get_pos()
		# these are all the positions around the node virtically and horizontally
		neighbors = [[col, row+1], [col, row-1], [col+1, row], [col-1, row]]

		if diagonals:
			# these are the diagonals for the node it that is turned on
			neighbors.extend(([col+1, row+1], [col-1, row-1], [col+1, row-1], [col-1, row+1]))

		#this is used to store values that don't exist on the grid
		neighbor_del = []
		# see if everything in neighbors is a real node that can be accessed
		for index,i in enumerate(neighbors):
			# the column and rows
			if i[0] < 0 or i[0] > COLUMNS-1 or i[1] < 0 or i[1] > ROWS-1:
				# save the values that fail
				neighbor_del.append(index)
			else:
				# replace the values that passed with the node it self on the grid
				neighbors[index] = grid[i[1]][i[0]]

		# pop all the values we can't use
		for i in neighbor_del:
			neighbors.pop(i)

		# what we will do to the neighbors
		for i in neighbors:
			# see if we the node is supposed to be ignored or not
			if i.walkable:
				# make g
				i.g = current_node.g + 1
				# set the heuristic value for the neighbor
				i.h = manhattanH(i.get_pos(), end.get_pos())
				# f is the sum of .g and .h
				i.f = i.g + i.h
				# the parent of the neighbor is the current node because it was the one that accessed it
				i.parent = current_node
				# so we don't switch end to a open node
				if i != end:
					# make it open
					i.make_open()
				# and add it to the open list
				openlist.append(i)

		# need this to see it run or else the function would finish instantly and nothing would be visualized
		draw()

		# take of the current node from open list
		openlist.pop(current_index)
		# add it to closed
		closedlist.append(current_node)
		# 
		if current_node != start:
			current_node.make_closed()

def main():
	# start and end nodes won't be placed yet
	start = None
	end = None
	# for ending the program it self
	run= True
	# if the A* is running or not
	started = False
	while run:
		draw()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run= False

			# reset the grid
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					# revert the values back
					started = False
					start = None
					end = None
					# change them all back
					for row in grid:
						for node in row:
							node.reset()

			#make it so not buttons can be pressed while A* is running			
			if started:
				continue

			# left mouse click
			if pygame.mouse.get_pressed()[0]:
				# getting the node from the clicked position
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos)
				spot = grid[row][col]
				# making a start if there isn't one already
				if not start and spot != end:
					start = spot
					start.make_start()
				
				# end if there isn't one already
				elif not end and spot != start:
					end = spot
					end.make_end()

				# make barrier if both exist
				elif spot != end and spot != start:
					spot.make_barrier()

			# right mouse button
			elif pygame.mouse.get_pressed()[2]:
				# get clicked pos
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos)
				spot = grid[row][col]
				#reset the spot
				spot.reset()
				# go back to the default values for start and end if they are clicked
				if spot == start:
					start = None
				elif spot == end:
					end = None
			
			#Space button
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
					#start A*
					started = True
					Astar(start, end)

			# turn on or off diagonals
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_d and not started:
					global diagonals
					if diagonals == True:
						diagonals = False
						pygame.display.set_caption('A* Path Finding Algorithm (no diagonals)')

					elif diagonals == False:
						diagonals = True
						pygame.display.set_caption('A* Path Finding Algorithm (diagonals)')

			pygame.event.get()

	pygame.quit()

main()