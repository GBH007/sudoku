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
		self.rows_on_set=[set() for i in range(9)]
		self.cols_on_set=[set() for i in range(9)]
		self.squs_on_set=[set() for i in range(9)]
		self.vp={i:[] for i in range(1,10)}
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
		on_set=set()
		for i in self.m[row]:
			on_set.add(i)
		return num_set-on_set
		
	def _noIncOnCol(self,col):
		on_set=set()
		for i in self.m:
			on_set.add(i[col])
		return num_set-on_set
		
	def _noIncOnSquare(self,srow,scol):
		on_set=set()
		for i in range(3):
			for j in range(3):
				on_set.add(self.m[srow*3+i][scol*3+j])
		return num_set-on_set
		
	def _getVarPos(self,num):
		l=[]
		for i in range(9):
			for j in range(9):
				if self.noIncOnCellNum(i,j,num):
					l.append((i,j))
		return l
		
	#not used
	
	def noIncOnCell(self,row,col):
		if self.m[row][col]:
			return set()
		on_set=num_set&self.noIncOnSquare(row//3,col//3)
		on_set&=self.noIncOnRow(row)
		on_set&=self.noIncOnCol(col)
		return on_set
		
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
	
	def noIncOnRow(self,row):
		return self.rows_on_set[row]
		
	def noIncOnCol(self,col):
		return self.cols_on_set[col]
		
	def noIncOnSquare(self,srow,scol):
		return self.squs_on_set[srow*3+scol]
		
	def noIncOnCellNum(self,row,col,num):
		if self.m[row][col]:
			return False
		return (num in self.noIncOnSquare(row//3,col//3))&(num in self.noIncOnRow(row))&(num in self.noIncOnCol(col))
		
	def getHashNum(self):
		return self.hn
		
	def getMinLostCountNum(self):
		hn=self.getHashNum()
		ans=None
		c=-1
		for i,e in enumerate(hn):
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
		hn=self.getHashNum()
		if hn[0]:
			return False
		return True
		
	def getVarPos(self,num):
		vp=[(i,j) for i,j in self.vp[num] if self.noIncOnCellNum(i,j,num)]
		return vp
		
	def set(self,row,col,val):
		self.rows_on_set[row].remove(val)
		self.cols_on_set[col].remove(val)
		self.squs_on_set[(row//3)*3+col//3].remove(val)
		self.hn[val]+=1
		self.hn[0]-=1
		self.m[row][col]=val
		
	def unset(self,row,col):
		val=self.m[row][col]
		self.rows_on_set[row].add(val)
		self.cols_on_set[col].add(val)
		self.squs_on_set[(row//3)*3+col//3].add(val)
		self.hn[val]-=1
		self.hn[0]+=1
		self.m[row][col]=0
		

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
gfile=open('data.txt','a')
ans_set=set()
def run(su,d=0):
	global ans_set
	#~ if su.complete() and su.ok():
	if su.complete():
		hs=su.getHashStr()
		if not hs in ans_set:
			ans_set.add(hs)
			print(hs,file=gfile)
			print('ex')
		return 0
	n=su.getMinLostCountNum()
	#~ print(d,n,len(ans_set))
	if len(ans_set)>0:
		return 0
	if not n:
		print('nm')
		return 0
	l=su.getVarPos(n)
	for i,j in l:
		#~ print(len(su.vp[n]))
		su.set(i,j,n)
		run(su,d+1)
		su.unset(i,j)
		#~ print(len(su.vp[n]))




def Run():
	#~ hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'			#209.	#101.6			#100.7
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097004'			#6.2	#1.8	#0.09
	hs='006000137900600508025381009102860700600053900390702850009146075460030091013097000'						#1.82	#0.1	#1.8
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097084'					#1.82	#0.02	#0.001
	s1=Sudoku()
	s1.setOnHashStr(hs)
	#~ s1.noIncPrec()
	t=time.time()
	run(s1)
	t=time.time()-t
	print(t)
	#~ print(s1.getHashNum())
	s2=Sudoku()
	s2.setOnHashStr(ans_set.pop())
	print(s2)
Run()
gfile.close()
