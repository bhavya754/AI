#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import time 
import sys 
ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
	"""Helper function to print board in a square."""
	print("-----------------")
	for i in ROW:
		row = ''
		for j in COL:
			row += (str(board[i + j]) + " ")
		print(row)


def board_to_string(board):
	"""Helper function to convert board dictionary to string for writing."""
	ordered_vals = []
	for r in ROW:
		for c in COL:
			ordered_vals.append(str(board[r + c]))
	return ''.join(ordered_vals)

def find_possible_vals(board, row, col):
	mp = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9}
	rev_mp = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I'}
	possible = {0,1,2,3,4,5,6,7,8,9}
	hor_present,ver_present,grid_present = set(),set(),set()
	for c in COL:
		hor_present.add(board[row + c])
	for r in ROW:
		ver_present.add(board[r + col])
	start_row = ((int(mp[row]) - 1) // 3) *3 + 1
	start_col =  ((int(col) - 1) // 3) *3 + 1
	temp = start_col
	for j in range(3):
		for i in range(3):
			grid_present.add(board[rev_mp[start_row ] + str(start_col + i)])
		start_row += 1
		start_col = temp
	pos = possible - hor_present.union(ver_present).union(grid_present)
	return list(pos)

# def LCV_heur(board,val,pos):

# 	changed = []
# 	for v in val:
# 		temp = board.copy()
# 		temp[pos] = v
# 		p = 0 
# 		for r in ROW:
# 			for c in COL:
# 				if(board[r+c] == 0) :	
# 					p = p + len(find_possible_vals(temp,r,c))
# 		changed.append((v,p))			

# 	def foo(x):
# 		return x[1]
# 	return sorted(changed,key = foo, reverse = True)


def MRV_heur(board):
	min_val = 999999
	state = None
	for r in ROW:
		for c in COL:
			if(board[r+c] == 0):
				possible = find_possible_vals(board, r,c)
				if len(possible) == 1:
					return ((str(r+c), possible, 1))
				if (len(possible) < min_val):
					min_val = len(possible)
					state = (str(r+c),possible,len(possible))

	return state

def foo(x):
	return x[1]

def backtracking(board):
	"""Takes a board and returns solved board."""
	# TODO: implement this
	var = MRV_heur(board.copy())
	#Termination condition 
	if var is None:
		return board
	lcv_arr = []
	for val in var[1]:
		temp = board.copy()
		temp[var[0]] = val
		ans = forward_check(temp)
		if ans < 0:
			return temp
		if ans:
			lcv_arr.append((val,ans))

	sorted_lcv = sorted(lcv_arr,key = foo,reverse = True)
	for v in sorted_lcv:
		v = v[0]
		board[var[0]] = v
		res = backtracking(board)
		if res:
			return res
		board[var[0]] = 0
	return None     

def forward_check(board):
	lcv_val = 0
	for r in ROW:
		for c in COL:
			if (board[r+c] == 0):
				temp = find_possible_vals(board,r,c)
				if len(temp) == 0:
					return False
				lcv_val += len(temp)
	if lcv_val == 0:
		return -1
	return lcv_val



if __name__ == '__main__':
	#  Read boards from source.

	src_filename = 'sudokus_start.txt'
	if sys.argv[1]:
		src_filename = sys.argv[1]
	try:
		srcfile = open(src_filename, "r")
		sudoku_list = srcfile.read()
	except:
		print("Error reading the sudoku file %s" % src_filename)
		exit()

	# Setup output file
	out_filename = 'output.txt'
	outfile = open(out_filename, "w")
	start = time.time()
	# Solve each board using backtracking
	for line in sudoku_list.split("\n"):

		if len(line) < 9:
			continue

		# Parse boards to dict representation, scanning board L to R, Up to Down
		board = { ROW[r] + COL[c]: int(line[9*r+c])
				  for r in range(9) for c in range(9)}

		# Print starting board. TODO: Comment this out when timing runs.
		print_board(board)

		# Solve with backtracking
		solved_board = backtracking(board)

		# Print solved board. TODO: Comment this out when timing runs.
		print_board(solved_board)
		
		# Write board to file
		outfile.write(board_to_string(solved_board))
		outfile.write('\n')
	end = time.time()
	print("Finishing all boards in file.")
	# print("Time:", (str(end - start)))