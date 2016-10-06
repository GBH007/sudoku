# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

from functions import get_miid

class Sudoku:
	
	def __init__(self,m=None):
		self.m=m if m else [[0 for j in range(9)]for i in range(9)]
		self.hvn=[]
		self.precalc()
		
	#precalc block

	def precalc(self):
		self.number_cache=[0 for i in range(10)]
		for l in self.m:
			for i in l:
				self.number_cache[i]+=1
				
		self.rows_cache=[[1 for i1 in range(10)] for i in range(9)]
		self.cols_cache=[[1 for i1 in range(10)] for i in range(9)]
		self.square_cache=[[1 for i1 in range(10)] for i in range(9)]
		
		for i in range(9):
			for j in range(9):
				self.rows_cache[i][self.m[i][j]]=0
				self.cols_cache[j][self.m[i][j]]=0
				self.square_cache[(i//3)*3+j//3][self.m[i][j]]=0
				
				
		self.vp=[[] for i in range(10)]
		for n in range(1,10):
			self.vp[n]=[(i,j) for i in range(9) for j in range(9) if self.getMCache(i,j,n)==1]
			
			
		self.hm={}
		for i in range(9):
			for j in range(9):
				if not self.m[i][j]:
					for n in range(1,10):
						if self.getMCache(i,j,n):
							if not (i,j) in self.hm:
								self.hm[(i,j)]=[]
							self.hm[(i,j)].append(n)
		self.hhm=[(len(self.hm[i]),i) for i in self.hm if len(self.hm[i])>0]
		self.hhm.sort()
							
		
		
	#not used
			
	def ok(self):
		rows=[[0 for i in range(10)] for j in range(9)]
		cols=[[0 for i in range(10)] for j in range(9)]
		squs=[[0 for i in range(10)] for j in range(9)]
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
				
	def getMCache(self,row,col,num):
		return 0 if self.m[row][col] else self.rows_cache[row][num]&self.cols_cache[col][num]&self.square_cache[(row//3)*3+col//3][num]
				
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
		if self.number_cache[0]:
			return False
		return True
		
	def getCellPosAndN(self,i):
		i1,j=i
		cp=[(i1,j,n) for n in self.hm[i] if self.getMCache(i1,j,n)]
		return cp
				
	def getVarPosAndN(self,num):
		vp=[(i,j,num) for i,j in self.vp[num] if self.getMCache(i,j,num)]
		return vp
		
		
	def set(self,row,col,val):
		self.rows_cache[row][val]=0
		self.cols_cache[col][val]=0
		self.square_cache[(row//3)*3+col//3][val]=0
		self.number_cache[val]+=1
		self.number_cache[0]-=1
		self.m[row][col]=val
		
	def unset(self,row,col):
		val=self.m[row][col]
		self.rows_cache[row][val]=1
		self.cols_cache[col][val]=1
		self.square_cache[(row//3)*3+col//3][val]=1
		self.number_cache[val]-=1
		self.number_cache[0]+=1
		self.m[row][col]=0
	
