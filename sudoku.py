# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
import copy
import time
num_set=set((1,2,3,4,5,6,7,8,9))
class Sudoku:
	def __init__(self,m=None):
		self.m=m if m else [[0 for j in range(9)]for i in range(9)]
		#hash number
		self.hn=[]
		self.rows_on_set=[[1 for i1 in range(10)] for i in range(9)]
		self.cols_on_set=[[1 for i1 in range(10)] for i in range(9)]
		self.squs_on_set=[[1 for i1 in range(10)] for i in range(9)]
		self.vp=[[] for i in range(10)]
		self.precalc()
		
	#precalc block

	def precalc(self):
		self.hn=self._getHashNum()
		
		for i in range(9):
			self.rows_on_set[i]=self._noIncOnRow(i)
			self.cols_on_set[i]=self._noIncOnCol(i)
		for i in range(3):
			for j in range(3):
				self.squs_on_set[i*3+j]=self._noIncOnSquare(i,j)
				
		for i in range(1,10):
			self.vp[i]=self._getVarPos(i)
			
	def _getHashNum(self):
		hs=[0 for i in range(10)]
		for l in self.m:
			for i in l:
				hs[i]+=1
		return hs
		
	def _noIncOnRow(self,row):
		on_set=[1 for i in range(10)]
		for i in self.m[row]:
			on_set[i]=0
		return on_set
		
	def _noIncOnCol(self,col):
		on_set=[1 for i in range(10)]
		for i in self.m:
			on_set[i[col]]=0
		return on_set
		
	def _noIncOnSquare(self,srow,scol):
		on_set=[1 for i in range(10)]
		for i in range(3):
			for j in range(3):
				on_set[self.m[srow*3+i][scol*3+j]]=0
		return on_set
		
	def _getVarPos(self,num):
		l=[]
		for i in range(9):
			for j in range(9):
				if self.noIncOnCellNum(i,j,num):
					l.append((i,j))
		return l
		
	#not used
			
	def ok(self):
		rows=[{i:0 for i in range(10)}for j in range(9)]
		cols=[{i:0 for i in range(10)}for j in range(9)]
		squs=[{i:0 for i in range(10)}for j in range(9)]
		for i in range(9):
			for j in range(9):
				rows[i][self.m[i][j]]+=1
				cols[j][self.m[i][j]]+=1
				squs[(i//3)*3+j//3][self.m[i][j]]+=1
		for i in range(9):
			for j in range(1,10):
				if rows[i][j]>1:return False
				if cols[i][j]>1:return False
				if squs[i][j]>1:return False
		return True
	
	#main block	
				
	def noIncOnCellNum(self,row,col,num):
		if self.m[row][col]:
			return False
		return self.rows_on_set[row][num]&self.cols_on_set[col][num]&self.squs_on_set[(row//3)*3+col//3][num]
				
	def getMinLostCountNum(self):
		ans=None
		c=-1
		for i,e in enumerate(self.hn):
			if i and (c<e<9):
				ans=i
				c=e
		return ans
		
	def getHashStr(self):
		return ''.join([''.join([str(i)for i in l])for l in self.m])
		
	def setOnHashStr(self,hs):
		for i in range(9):
			for j in range(9):
				self.m[i][j]=int(hs[i*9+j])
		self.precalc()
		
	def __str__(self):
		return '\n'.join([' '.join([str(i)for i in l])for l in self.m])
		
	def complete(self):
		if self.hn[0]:
			return False
		return True
		
	def getVarPos(self,num):
		vp=[(i,j) for i,j in self.vp[num] if self.noIncOnCellNum(i,j,num)]
		return vp
		
	def set(self,row,col,val):
		self.rows_on_set[row][val]=0
		self.cols_on_set[col][val]=0
		self.squs_on_set[(row//3)*3+col//3][val]=0
		self.hn[val]+=1
		self.hn[0]-=1
		self.m[row][col]=val
		
	def unset(self,row,col):
		val=self.m[row][col]
		self.rows_on_set[row][val]=1
		self.cols_on_set[col][val]=1
		self.squs_on_set[(row//3)*3+col//3][val]=1
		self.hn[val]-=1
		self.hn[0]+=1
		self.m[row][col]=0
	
