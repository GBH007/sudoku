# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

def get_miid(l):
	me=l[0]
	mi=0 if l[0]>0 else -1
	for i,e in enumerate(l):
		if 0<e and(e<me or me<=0):
			me=e
			mi=i
	return mi

class SQueue:
	
	def __init__(self,su):
		self.sudoku=su
		self.stack=[]
		
	def add(self,data,l):
		self.stack.append((l,data))
		
	def set(self):
		l,data=self.stack[-1]
		if l==0:
			self.sudoku.set(data[0],data[1],data[2])
		elif l==1:
			self.sudoku.set(data[0][0],data[0][1],data[0][2])
			
	def unset(self):
		l,data=self.stack[-1]
		if l==0:
			self.sudoku.unset(data[0],data[1])
			self.stack.pop()
		elif l==1:
			self.sudoku.unset(data[0][0],data[0][1])
			self.stack[-1][1].pop(0)
			if len(self.stack[-1][1])==0:
				self.stack.pop()
				l=0
		return l
		
	def __len__(self):
		return len(self.stack)

class CellNumPlaceCountSortedList:
	def __init__(self,l=None):
		self._l=[] if not l else sorted(l)
		self.l_len=len(self._l)
	def add(self,e):
		self.l_len+=1
		if self.l_len==1:
			self._l.append(e)
			return 0
		l=0
		r=self.l_len-1
		while(r-l>1):
			m=(l+r)//2
			if self._l[m][0]>e[0]:
				r=m
			elif self._l[m][0]<e[0]:
				l=m
			elif self._l[m][0]==e[0]:
				l=m
				r=m
				break
		if self._l[l][0]>=e[0]:
			self._l.insert(l,e)
		else:
			self._l.insert(r,e)
		
	def pop(self):
		e=self._l[0]
		self.l_len-=1
		del self._l[0]
		return e
		
	def getCount(self):
		return self._l[0][0]
		
	def getI(self):
		return self._l[0][1]
		
	def __len__(self):return self.l_len
		
	def __str__(self):return str(self._l)


if __name__=='__main__':
	l=CellNumPlaceCountSortedList([(1,0),(3,0),(5,0),(6,0),(7,0),(8,0),(9,0)])
	print(l)
	l.add((2,0))
	l.add((4,0))
	l.add((8,0))
	l.add((-8,0))
	print(l)
	print(l.pop())
	print(l.pop())
	print(l)
	
	l.add((2,0))
	l.add((4,0))
	l.add((8,0))
	l.add((-8,0))
	print(l)
	#~ print(l)
