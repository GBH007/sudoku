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
