
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
from collections import deque
from hashlib import sha1
import hashlib
import numpy as np
import heapq
import resource
import os 

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
	"""
		The PuzzleState stores a board configuration and implements
		movement instructions to generate valid children.
	"""
	def __init__(self, config, n, parent=None, action="Initial", cost=0):
		"""
		:param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
		:param n->int : Size of the board
		:param parent->PuzzleState
		:param action->string
		:param cost->int
		"""
		if n*n != len(config) or n < 2:
			raise Exception("The length of config is not correct!")
		if set(config) != set(range(n*n)):
			raise Exception("Config contains invalid/duplicate entries : ", config)

		self.n        = n
		self.cost     = cost
		self.parent   = parent
		self.action   = action
		self.config   = config
		self.children = []

		# Get the index and (row, col) of empty block
		self.blank_index = self.config.index(0)

	def display(self):
		""" Display this Puzzle state as a n*n board """
		for i in range(self.n):
			print(config[3*i : 3*(i+1)])

	def move_up(self):
		""" 
		Moves the blank tile one row up.
		:return a PuzzleState with the new configuration
		"""

		n=self.n
		cfg = self.config[:]
		if self.blank_index < n:
			return None
		temp=cfg[self.blank_index - n]
		cfg[self.blank_index - n] = 0
		cfg[self.blank_index] = temp
		new_obj=PuzzleState(cfg,self.n, self, "Up",self.cost+1)
		# print(new_obj.cfg)
		return new_obj
	  
	def move_down(self):
		"""
		Moves the blank tile one row down.
		:return a PuzzleState with the new configuration
		"""
		n=self.n
		cfg = self.config[:]
		if self.blank_index >= (n ** 2 - n):
			return None
		temp=cfg[self.blank_index + n]
		cfg[self.blank_index + n] = 0
		cfg[self.blank_index] = temp
		# print(temp)
		# print(cfg)
		new_obj=PuzzleState(cfg,self.n, self,"Down",self.cost+1)
		return new_obj
	  
	def move_left(self):
		"""
		Moves the blank tile one column to the left.
		:return a PuzzleState with the new configuration
		"""
		n=self.n
		cfg = self.config[:]
		if self.blank_index % n == 0:
			return None
		temp=cfg[self.blank_index -1]
		cfg[self.blank_index -1] = 0
		cfg[self.blank_index] = temp
		new_obj=PuzzleState(cfg,self.n, self, "Left",self.cost+1)
		return new_obj

	def move_right(self):
		"""
		Moves the blank tile one column to the right.
		:return a PuzzleState with the new configuration
		"""
		n=self.n
		cfg = self.config[:]
		if (self.blank_index + 1) % n == 0:
			return None
		temp=cfg[self.blank_index +1]
		cfg[self.blank_index +1] = 0
		cfg[self.blank_index] = temp
		new_obj=PuzzleState(cfg,self.n, self, "Right",self.cost+1)
		return new_obj
	  
	def expand(self):
		""" Generate the child nodes of this node """
		
		# Node has already been expanded
		if len(self.children) != 0:
			return self.children
		
		# Add child nodes in order of UDLR
		children = [
			self.move_up(),
			self.move_down(),
			self.move_left(),
			self.move_right()]

		# Compose self.children of all non-None children states
		self.children = [state for state in children if state is not None]
		return self.children

	def tilehash(self):
		return sha1(np.asarray(self.config)).hexdigest()
# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(goal_state,nodes,depth,max_depth,time):
	### Student Code Goes here
	path=[]
	gls=goal_state
	cfgs=[]

	while goal_state.parent != None:
		path.append(goal_state.action)
		cfgs.append(goal_state.config)
		goal_state= goal_state.parent
	path.reverse()

	if os.path.exists('output.txt'):
		aw = 'a' 
	else:
		aw = 'w' 
	file = open('output.txt',aw)
	file.write("path_to_goal: " + str(path))
	file.write("\ncost_of_path: " + str(gls.cost))
	file.write("\nnodes_expanded: " + str(nodes))
	file.write("\nsearch_depth: " + str(gls.cost))
	file.write("\nmax_search_depth: " + str(max_depth))
	file.write("\nrunning_time: " + format(time, '.8f'))
	file.write("\nmax_ram_usage: " + format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0, '.8f'))    
	file.close()
	# print("cfgs",cfgs)

def bfs_search(initial_state):
	"""BFS search"""
	### STUDENT CODE GOES HERE ###
	max_depth=0
	iterations = 0 # Only for stats.
	visited = set()
	queue = deque([initial_state])
	search_depth=0
	while queue :
		node = queue.popleft()
		visited.add(str(node.config))

		if test_goal(node):
			return node,iterations,search_depth,max_depth
		children = node.expand()
		iterations+=1
		for child in children:
			# print(child.config)
			
			if str(child.config) not in visited:
				if max_depth < child.cost:
					max_depth=child.cost
				queue.append(child)
				visited.add(str(child.config))

		# print(len(queue))
	print("not found")
	return 
def dfs_search(initial_state):
	"""DFS search"""
	### STUDENT CODE GOES HERE ###
	max_depth=0
	q = [initial_state]
	nodes_expanded = 0
	search_depth=0
	visited = set()
	visited.add(str(initial_state.config))
	while q:
		popped = q.pop()
		if test_goal(popped):
			return popped,nodes_expanded,search_depth,max_depth
			
		children = popped.expand()
		children.reverse()
		nodes_expanded += 1
		# search_depth +=1
		for child in children:
			if str(child.config) not in visited:
				if max_depth < child.cost:
					max_depth=child.cost
				q.append(child)
				visited.add(str(child.config))
		# print(visited)
	print('No solution')
	return

def A_star_search(initial_state):
	"""A * search"""
	### STUDENT CODE GOES HERE ###
	max_depth=0
	iterations = 0 # Only for stats.
	visited = set()
	heap = []
	search_depth=0
	heapq.heappush(heap,(0,0,initial_state))
	child_count=0
	while len(heap)>0 :
		node = heapq.heappop(heap)[2]
		visited.add(str(node.config))
		if test_goal(node):
			return node,iterations,search_depth,max_depth
		children = node.expand()
		iterations+=1
		temp = []
		for child in children:
			if str(child.config) not in visited:
				if max_depth < child.cost:
					max_depth=child.cost
				tmp=calculate_total_cost(child)
				heapq.heappush(heap,(tmp,child_count,child))
				visited.add(str(child.config))
			child_count+=1
	print("not found")
	return 
def calculate_total_cost(state):
	"""calculate the total estimated cost of a state"""
	### STUDENT CODE GOES HERE ###
	man_dist = 0
	for i in range(9):
		man_dist += calculate_manhattan_dist(i,state.config[i],3)
	return man_dist + state.cost

def calculate_manhattan_dist(idx,value,n):
	"""calculate the manhattan distance of a tile"""
	### STUDENT CODE GOES HERE ###
	map = {}
	map[0] = (0,0)
	map[1] = (0,1)
	map[2] = (0,2)
	map[3] = (1,0)
	map[4] = (1,1)
	map[5] = (1,2)
	map[6] = (2,0)
	map[7] = (2,1)
	map[8] = (2,2)
	return abs(map[idx][0] - map[value][0]) + abs(map[idx][1] - map[value][1])

def test_goal(puzzle_state):
	"""test the state is the goal state or not"""
	### STUDENT CODE GOES HERE ###
	goal = [0,1,2,3,4,5,6,7,8]
	if puzzle_state.config == goal:
		return True
	return False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
	search_mode = sys.argv[1].lower()
	begin_state = sys.argv[2].split(",")
	begin_state = list(map(int, begin_state))
	board_size  = int(math.sqrt(len(begin_state)))
	hard_state  = PuzzleState(begin_state, board_size)
	start_time  = time.time()
	
	if   search_mode == "bfs": a,b,c,d=bfs_search(hard_state)
	elif search_mode == "dfs": a,b,c,d=dfs_search(hard_state)
	elif search_mode == "ast": a,b,c,d=A_star_search(hard_state)
	else: 
		print("Enter valid command arguments !")
		
	end_time = time.time()
	writeOutput(a,b,c,d,(end_time-start_time))
	# print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
	main()