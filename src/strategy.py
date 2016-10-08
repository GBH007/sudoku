# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

from .functions import get_miid,get_meid9
from .sudoku import CacheController
import itertools

class Strategy:
	
	def __init__(self,su):
		self.su=su
		self.counter=0
		
	def getEff(self):
		#возврашает количество вариантов хода по стратегии (чем меньше тем лчше, если =<0 то стратегия не работает)
		pass
		
	def getDataToQueue(self):
		#возврашает варианты хода 0-*
		pass
	
	def getMCache(self,row,col,num):
		return 0 if self.su.m[row][col] else self.su.rows_cache[row][num]&self.su.cols_cache[col][num]&self.su.square_cache[(row//3)*3+col//3][num]
		
	def getUseCount(self,row,col,num):
		s=0
		sis=(row//3)*3
		sie=sis+2
		sjs=(col//3)*3
		sje=sjs+2
		for i in range(9):
			if (i<sis or i>sie) and self.getMCache(i,col,num):
				s+=1
			if (i<sjs or i>sje) and self.getMCache(row,i,num):
				s+=1
			if self.getMCache((row//3)*3+i//3,(col//3)*3+i%3,num):
				s+=1
			if i+1!=num and self.getMCache(row,col,i+1)==1:
				s+=1
		return s
		
class MaxPlaceCountStrategy(Strategy):
	
	name='MaxPlaceCountStrategy'
			
	def getEff(self):
		self.n=get_meid9(self.su.number_cache)
		return self.su.cpon_cache[self.n] if self.n else 0

	def getDataToQueue(self):
		self.counter+=1
		#~ return sorted([(i,j,self.n) for i,j in self.su.pon_cache[self.n]],key=lambda x: self.su.ncc_cache[x[0]*9+x[1]]) if self.n>0 else []
		return sorted([(i,j,self.n) for i,j in self.su.pon_cache[self.n]],key=lambda x: self.getUseCount(x[0],x[1],x[2]),reverse=0) if self.n>0 else []
		#~ return [(i,j,self.n) for i,j in self.su.pon_cache[self.n]] if self.n>0 else []
		
	def getBestData(self):
		self.counter+=1
		self.n=get_meid9(self.su.number_cache)
		if self.n<1: return []
		return [(self.getUseCount(i,j,self.n),(i,j,self.n)) for i,j in self.su.pon_cache[self.n]]

class MinLostVarCountStrategy(Strategy):
	
	name='MinLostVarCountStrategy'
				
	def getEff(self):
		self.n=get_miid(self.su.cpon_cache)
		if self.n>0:
			s=self.su.cpon_cache[self.n]
		else:
			s=-1
		return s
		
	def getDataToQueue(self):
		self.counter+=1
		#~ return sorted([(i,j,self.n) for i,j in self.su.pon_cache[self.n]],key=lambda x: self.su.ncc_cache[x[0]*9+x[1]]) if self.n>0 else []
		return sorted([(i,j,self.n) for i,j in self.su.pon_cache[self.n]],key=lambda x: self.getUseCount(x[0],x[1],x[2]),reverse=0) if self.n>0 else []
		#~ return [(i,j,self.n) for i,j in self.su.pon_cache[self.n]] if self.n>0 else []
		
	def getBestData(self):
		self.counter+=1
		self.n=get_miid(self.su.cpon_cache)
		if self.n<1: return []
		return [(self.getUseCount(i,j,self.n),(i,j,self.n)) for i,j in self.su.pon_cache[self.n]]
		
class MinCellPlaceStrategy(Strategy):
	
	name='MinCellPlaceStrategy'
			
	def getEff(self):
		self.i=get_miid(self.su.ncc_cache)
		self.c=-1 if self.i<0 else self.su.ncc_cache[self.i]
		return self.c
		
	def getDataToQueue(self):
		self.counter+=1
		if self.c<1:
			return []
		i=self.i//9
		j=self.i%9
		#~ return sorted([(i,j,n) for n in range(1,10) if self.getMCache(i,j,n)],key=lambda x: self.su.cpon_cache[x[2]])
		return sorted([(i,j,n) for n in range(1,10) if self.getMCache(i,j,n)],key=lambda x: self.getUseCount(x[0],x[1],x[2]),reverse=0)
		#~ return [(i,j,n) for n in range(1,10) if self.getMCache(i,j,n)]
		
	def getBestData(self):
		self.counter+=1
		self.i=get_miid(self.su.ncc_cache)
		if self.i<0: return []
		i=self.i//9
		j=self.i%9
		return [(self.getUseCount(i,j,n),(i,j,n)) for n in range(1,10) if self.getMCache(i,j,n)]


_ALL_STRATEGYS=[
	MinCellPlaceStrategy,
	MaxPlaceCountStrategy,
	MinLostVarCountStrategy,
]


class Controller:
	
	def __init__(self,su,strategy_list=_ALL_STRATEGYS,strategy_weight=[1,3,3]):
		self.su=su
		self.cc=CacheController(self.su)
		self.st=[i(self.su) for i in strategy_list]
		#~ self.n0c=self.su.number_cache[0]
		#~ self.n0c=81
		self.stw=strategy_weight
		self.hash=None
		self.operation_stack=[]
		
	def getMostEffQueue1(self):
		s=[]
		for st in self.st:
			s+=st.getBestData()
		s=list(set(s))
		s.sort(reverse=0)
		#~ print(s)
		#~ raise Exception
		#~ s.sort()
		#~ print(s)
		return [i[1] for i in s[:5]]
	def getMostEffQueue(self):
		#~ n0c=(self.n0c-self.su.number_cache[0])/self.n0c
		#~ n0c=(-(n0c*2-1)**2+1)
		#~ stw=[e-2*n0c if i!=0 else e for i,e in enumerate(self.stw)]
		#~ feff=[e.getEff()*stw[i] for i,e in enumerate(self.st)]
		feff=[e.getEff()*self.stw[i] for i,e in enumerate(self.st)]
		miid=get_miid(feff)
		if miid==-1:
			return []
		return self.st[miid].getDataToQueue()
		
	def run(self):
		try:
			while 1:
				if self.complete() and self.suOk():
					self.hash=self.su.getHashStr()
					return 1
				#~ if self.brokenFieldCheck():
				if 40>self.su.number_cache[0]>30 and self.brokenFieldCheck():
					self.unset()
					self.set()
					continue
				l=self.getMostEffQueue()
				if not l:
					self.unset()
				else:
					self.operation_stack.append((1,l))
				self.set()
		except IndexError:
			self.stw=[1,7,7]
			self.run()
			
	def complete(self):
		return False if self.su.number_cache[0] else True
	
	def brokenFieldCheck(self):
		for i in range(1,10):
			if self.su.cpon_cache[i]+self.su.number_cache[i]-9<0:
				#~ print(self.su.cpon_cache[i]+self.su.number_cache[i]-9,self.su.cpon_cache,self.su.number_cache,i)
				#~ raise Exception
				return True
		return False
	
	def set(self):
		l,data=self.operation_stack[-1]
		if l==0:
			self.su.m[data[0]][data[1]]=data[2]
			self.cc.set(data[0],data[1],data[2])
		elif l==1:
			self.su.m[data[0][0]][data[0][1]]=data[0][2]
			self.cc.set(data[0][0],data[0][1],data[0][2])
			
	def unset(self):
		l=0
		while not l:
			l,data=self.operation_stack[-1]
			if l==0:
				self.su.m[data[0]][data[1]]=0
				self.cc.unset(data[0],data[1],data[2])
				self.operation_stack.pop()
			elif l==1:
				self.su.m[data[0][0]][data[0][1]]=0
				self.cc.unset(data[0][0],data[0][1],data[0][2])
				self.operation_stack[-1][1].pop(0)
				if len(self.operation_stack[-1][1])==0:
					self.operation_stack.pop()
					l=0
	
	def suOk(self):
		rows=[[0 for i in range(10)] for j in range(9)]
		cols=[[0 for i in range(10)] for j in range(9)]
		squs=[[0 for i in range(10)] for j in range(9)]
		for i in range(9):
			for j in range(9):
				rows[i][self.su.m[i][j]]+=1
				cols[j][self.su.m[i][j]]+=1
				squs[(i//3)*3+j//3][self.su.m[i][j]]+=1
		for i in range(9):
			for j in range(1,10):
				if rows[i][j]>1:return False
				if cols[i][j]>1:return False
				if squs[i][j]>1:return False
		return True
		
	def __str__(self):
		return '\n'.join(['{0.name}  {0.counter}'.format(i) for i in self.st])

