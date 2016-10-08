# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

from .functions import get_miid

class SudokuData:
	
	def __init__(self,m=None):
		self.m=m if m else [[0 for j in range(9)]for i in range(9)]
										
	def getHashStr(self):
		return ''.join([''.join([str(i)for i in l])for l in self.m])
		
	def setOnHashStr(self,hs):
		for i in range(9):
			for j in range(9):
				self.m[i][j]=int(hs[i*9+j])
		
	def __str__(self):
		return '\n'.join([' '.join([str(i)for i in l])for l in self.m])
		

class CacheController:
	def __init__(self,su):
		self.su=su
				
		self.su.number_cache=[0 for i in range(10)]
		for l in self.su.m:
			for i in l:
				self.su.number_cache[i]+=1
				
		self.su.rows_cache=[[1 for n in range(10)] for i in range(9)]
		self.su.cols_cache=[[1 for n in range(10)] for i in range(9)]
		self.su.square_cache=[[1 for n in range(10)] for i in range(9)]
		
		for i in range(9):
			for j in range(9):
				self.su.rows_cache[i][self.su.m[i][j]]=0
				self.su.cols_cache[j][self.su.m[i][j]]=0
				self.su.square_cache[(i//3)*3+j//3][self.su.m[i][j]]=0
				
		self.su.m_cube_cache=[[[1 for l in range(10)] for j in range(9)]for i in range(9)]
		for i in range(9):
			for j in range(9):
				for n in range(1,10):
					self.su.m_cube_cache[i][j][n]=self.getMCache(i,j,n)
		
		#position of number cache
		self.su.pon_cache=[[] for i in range(10)]
		for n in range(1,10):
			self.su.pon_cache[n]=[(i,j) for i in range(9) for j in range(9) if self.getMCache(i,j,n)==1]
			
		#count position of numeber cache
		self.su.cpon_cache=[len([1 for i,j in self.su.pon_cache[num]]) for num in range(10)]
			
		self.su.free_cell_cache=[]
		for i in range(9):
			for j in range(9):
				if not self.su.m[i][j]:
					self.su.free_cell_cache.append((i,j))
		
		#number count on cell cache			
		self.su.ncc_cache=[sum([1 for n in range(1,10) if self.getMCache(i//9,i%9,n)==1]) for i in range(81)]	
		
	def getMCache(self,row,col,num):
		return 0 if self.su.m[row][col] else self.su.rows_cache[row][num]&self.su.cols_cache[col][num]&self.su.square_cache[(row//3)*3+col//3][num]
				
	def set(self,row,col,val):
		self.su.rows_cache[row][val]=0
		self.su.cols_cache[col][val]=0
		self.su.square_cache[(row//3)*3+col//3][val]=0
		for i in range(9):
			if self.su.m_cube_cache[i][col][val]==1:
				self.su.ncc_cache[i*9+col]-=1
				self.su.m_cube_cache[i][col][val]=0
				if (i,col) in self.su.pon_cache[val]:
					self.su.pon_cache[val].remove((i,col))
					self.su.cpon_cache[val]-=1
			if self.su.m_cube_cache[row][i][val]==1:
				self.su.ncc_cache[row*9+i]-=1
				self.su.m_cube_cache[row][i][val]=0
				if (row,i) in self.su.pon_cache[val]:
					self.su.pon_cache[val].remove((row,i))
					self.su.cpon_cache[val]-=1
			if self.su.m_cube_cache[(row//3)*3+i//3][(col//3)*3+i%3][val]==1:
				self.su.ncc_cache[((row//3)*3+i//3)*9+(col//3)*3+i%3]-=1
				self.su.m_cube_cache[(row//3)*3+i//3][(col//3)*3+i%3][val]=0
				if ((row//3)*3+i//3,(col//3)*3+i%3) in self.su.pon_cache[val]:
					self.su.pon_cache[val].remove(((row//3)*3+i//3,(col//3)*3+i%3))
					self.su.cpon_cache[val]-=1
		self.su.ncc_cache[row*9+col]=0
		for n in range(1,10):
			if (row,col) in self.su.pon_cache[n]:
				self.su.pon_cache[n].remove((row,col))
				self.su.cpon_cache[n]-=1
		
		self.su.number_cache[val]+=1
		self.su.number_cache[0]-=1
		
	def unset(self,row,col,val):
		self.su.rows_cache[row][val]=1
		self.su.cols_cache[col][val]=1
		self.su.square_cache[(row//3)*3+col//3][val]=1
		for i in range(9):
			if self.getMCache(i,col,val)==1:
				self.su.ncc_cache[i*9+col]+=1
				self.su.m_cube_cache[i][col][val]=1
				if (i,col) not in self.su.pon_cache[val]:
					self.su.pon_cache[val].append((i,col))
					self.su.cpon_cache[val]+=1
			if self.getMCache(row,i,val)==1:
				self.su.ncc_cache[row*9+i]+=1
				self.su.m_cube_cache[row][i][val]=1
				if (row,i) not in self.su.pon_cache[val]:
					self.su.pon_cache[val].append((row,i))
					self.su.cpon_cache[val]+=1
			if self.getMCache((row//3)*3+i//3,(col//3)*3+i%3,val)==1:
				self.su.ncc_cache[((row//3)*3+i//3)*9+(col//3)*3+i%3]+=1
				self.su.m_cube_cache[(row//3)*3+i//3][(col//3)*3+i%3][val]=1
				if ((row//3)*3+i//3,(col//3)*3+i%3) not in self.su.pon_cache[val]:
					self.su.pon_cache[val].append(((row//3)*3+i//3,(col//3)*3+i%3))
					self.su.cpon_cache[val]+=1
		self.su.ncc_cache[row*9+col]=sum(self.su.m_cube_cache[row][col])
		for n in range(1,10):
			if (self.getMCache(row,col,n)) and ((row,col) not in self.su.pon_cache[n]):
				self.su.pon_cache[n].append((row,col))
				self.su.cpon_cache[n]+=1
				
		self.su.number_cache[val]-=1
		self.su.number_cache[0]+=1
