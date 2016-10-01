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
	def noIncOnRow(self,row):
		on_set=set()
		for i in self.m[row]:
			on_set.add(i)
		return num_set-on_set
	def noIncOnCol(self,col):
		on_set=set()
		for i in self.m:
			on_set.add(i[col])
		return num_set-on_set
	def noIncOnSquare(self,srow,scol):
		on_set=set()
		for i in range(3):
			for j in range(3):
				on_set.add(self.m[srow*3+i][scol*3+j])
		return num_set-on_set
	def noIncOnCell(self,row,col):
		if self.m[row][col]:
			return set()
		on_set=self.noIncOnSquare(row//3,col//3)
		on_set&=self.noIncOnRow(row)
		on_set&=self.noIncOnCol(col)
		return on_set
	def getHashNum(self):
		hs={i:0 for i in num_set}
		for l in self.m:
			for i in l:
				if i:
					hs[i]+=1
		return hs
	def getMinLostCountNum(self):
		nl=sorted(self.getHashNum().items(),key=lambda x:x[1],reverse=True)
		ans=None
		for i,j in nl:
			if j!=9:
				ans=i
				break
		return ans
	def getHashStr(self):
		return ''.join([''.join([str(i)for i in l])for l in self.m])
	def setOnHashStr(self,hs):
		for i in range(9):
			for j in range(9):
				self.m[i][j]=int(hs[i*9+j])
	def __str__(self):
		return '\n'.join([' '.join([str(i)for i in l])for l in self.m])
	def complete(self):
		for l in self.m:
			for i in l:
				if not i:
					return False
		return True
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
	def getVarPos(self,num):
		l=[]
		for i in range(9):
			for j in range(9):
				if num in self.noIncOnCell(i,j):
					l.append((i,j))
		return l
	def set(self,row,col,val):
		self.m[row][col]=val
	def unset(self,row,col):
		self.m[row][col]=0

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
gfile=open('data.txt','a')
ans_set=set()
def run(su,d=0):
	global ans_set
	if su.complete() and su.ok():
		hs=su.getHashStr()
		if not hs in ans_set:
			ans_set.add(hs)
			print(hs,file=gfile)
		return 0
	n=su.getMinLostCountNum()
	print(d,n,len(ans_set))
	if len(ans_set)>0:return 0
	if not n:return 0
	l=su.getVarPos(n)
	if not l:
		return 0
	for i,j in l:
		#~ su1=copy.deepcopy(su)
		#~ su1.set(i,j,n)
		#~ run(su1,d+1)
		su.set(i,j,n)
		run(su,d+1)
		su.unset(i,j)





#~ def Run(hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'):
def Run(hs='006000137900600508025381009102860700600053900390702850009146075460030091013097004'):
	s1=Sudoku()
	s1.setOnHashStr(hs)
	#~ run(s1)
	t=time.time()
	run(s1)
	t=time.time()-t
	print(t)
	s2=Sudoku()
	s2.setOnHashStr(ans_set.pop())
	print(s2)
Run()
gfile.close()
