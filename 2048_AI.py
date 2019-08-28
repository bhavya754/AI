import time
from BaseAI_3 import BaseAI
import math
import sys
import random 

DEPTH_LIM =3

class PlayerAI(BaseAI):
		
	def getMove(self,grid):
		alpha = math.inf * -1
		beta = math.inf
		depth = 1
		final_move = self.max((grid,None),alpha,beta,depth, time.process_time())
		return final_move[0][1]

	def max(self,state,alpha,beta,depth,t1):
		if time.process_time() - t1 >= 0.18:
			val = self.eval(state[0])
			return (state,val)

		if depth == DEPTH_LIM:
			val = self.eval(state[0])
			return (state,val)
		# print("in max")
		max_child = None
		max_val = math.inf * -1

		if(len(state[0].getAvailableMoves()) ==0 ):
			val = self.eval(state[0])
			return (state,val)

		for m in state[0].getAvailableMoves():
			move=m[0]
			cloned = state[0].clone()
			cloned.move(move)
			_, util = self.min((cloned,move),alpha,beta,depth+1,t1)
			if util>max_val:
				max_child = (cloned,move)
				max_val = util
			if max_val >= beta:
				break
			if max_val > alpha:
				alpha = max_val

		return (max_child, max_val)


	def min(self,state,alpha,beta,depth,t1):
		if time.process_time() - t1 >= 0.18:
			val = self.eval(state[0])
			return (state,val)

		if depth == DEPTH_LIM:
			val = self.eval(state[0])
			return (state,val)
		# print("in min")
		min_child = None
		min_val = math.inf 
		if(len(state[0].getAvailableCells()) ==0 ):
			val = self.eval(state[0])
			return (state,val)
		for cell in state[0].getAvailableCells():
			cloned = state[0].clone()
			cloned.setCellValue(cell,2)
			_,val2 = self.max((cloned,None),alpha,beta,depth,t1)
			val2*=0.9
			cloned = state[0].clone()
			cloned.setCellValue(cell,4)
			_, val4 = self.max((cloned,None),alpha,beta,depth,t1)
			val4*=0.1
			val = val2+val4
			if val < min_val:
				min_child = (cloned,None)
				min_val = val
			if min_val <= alpha:
				break
			if min_val < beta:
				beta = min_val

		return (min_child, min_val)

	def strictly_increasing(self,L):
		return all(x<y for x, y in zip(L, L[1:]))

	def strictly_decreasing(self,L):
		return all(x>y for x, y in zip(L, L[1:]))

	def non_increasing(self,L):
		return all(x>=y for x, y in zip(L, L[1:]))

	def non_decreasing(self,L):
		return all(x<=y for x, y in zip(L, L[1:]))

	def monotonic(self,L):
		return self.non_increasing(L) or self.non_decreasing(L)

	def eval(self,grid):
		# print("in eval")
		val1 = len(grid.getAvailableCells()) * 2
		val2 = 0 
		if grid.map[0][0] == grid.getMaxTile():
			val2+=1
		if grid.map[0][3] == grid.getMaxTile():
			val2+=1
		if grid.map[3][0] == grid.getMaxTile():
			val2+=1
		if grid.map[3][3] == grid.getMaxTile():
			val2+=1

		grid_mask = [[4096,1024,256,64],
				[1024,256,64,16],
				[256,64,16,4],
				[64,16,4,1]]

		val5 = 0
		# # apply grid_mask
		for row in range(3):
			for column in range(3):
				val5 += grid.map[row][column] * grid_mask[row][column]
		val4=0
		for i in range(3):
			if self.monotonic(grid.map[i]): val4+=1
		for i in range(3):
			if self.monotonic(grid.map[:][i]): val4+=1


		val3 = 0
		for i in range(3):
			for j in range(3):
				if grid.map[i][j] == grid.map[i][j+1]:
					val3 += 1
				if grid.map[i][j] == grid.map[i+1][j]:
					val3 += 1 
		# print(val1,val2,val3,val4, val5/10000)
		return val3 + val5/10000



























