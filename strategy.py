# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

from functions import get_miid,SQueue

class Strategy:
	def __init__(self,su):
		self.su=su
	def getEff(self):
		#возврашает количество вариантов хода по стратегии (чем меньше тем лчше, если =<0 то стратегия не работает)
		pass
	def getFastEff(self):
		#тоже что и getEff только является приблизительной оценкой для первичного выбора
		pass
	def getDataToQueue(self):
		#возврашает варианты хода 0-*
		return self.su.getVarPosAndN(self.n)
	
class MaxPlaceCountStrategy(Strategy):
	def getEff(self):
		return self.eff
	def getFastEff(self):
		self.n=self.su.getMinLostCountNum()
		self.eff=9-self.su.hn[self.n] if self.n else 0
		return self.eff
		
class MinLostVarCountStrategy(Strategy):
	def getFastEff(self):
		self.n=self.su.getMinPlaceCountNum()
		return self.su.hvn[self.n] if self.n>0 else self.n
	def getEff(self):
		self.n=self.su._getMinPlaceCountNum()
		return self.su.hvn[self.n] if self.n>0 else self.n
	


_ALL_STRATEGYS=[
	MaxPlaceCountStrategy,
	MinLostVarCountStrategy,
]


class Strategys:
	def __init__(self,su,strategy_list=_ALL_STRATEGYS):
		self.su=su
		self.st=[i(self.su) for i in strategy_list]
		self.sq=SQueue(su)
		self.hasn=None
		
	def getMostEffQueue(self):
		feff=[i.getFastEff() for i in self.st]
		miid=get_miid(feff)
		if miid==-1:
			return []
		while 1:
			feff[miid]=self.st[miid].getEff()
			miid1=get_miid(feff)
			if miid==miid1:
				break
			else:
				miid=miid1
		return self.st[miid].getDataToQueue()
		
	def run(self):
		while 1:
			if self.su.complete():
				self.hasn=self.su.getHashStr()
				return 1
			l=self.getMostEffQueue()
			if not l:
				while not self.sq.unset():pass
			else:
				self.sq.add(l,1)
			self.sq.set()
