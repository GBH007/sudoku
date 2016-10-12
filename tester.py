# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
import src.strategy as strategy
from src import SudokuData
from src import Controller
import time

strat=[
	strategy.MinCellPlaceStrategy,
	strategy.MaxPlaceCountStrategy,
	strategy.MinLostVarCountStrategy,
]

_hs=[
	'000030002004000009000051040040320090002108300050046010030560000500000400200090000',
	'000040700031500006600037090000093025000000000950680000080310009400008630003060000',
	'006000137900600508025381009102860700600053900390702850009146075460030091013097000',
	'020003000405209000070008532102000000080000020000000304913500040000906803000300070',
	'482700100000043000300100900031000005090000030800000670003004006000370000005009312',
]

def _run(hs,fp=0):
	su=SudokuData()
	su.setOnHashStr(hs)
	c=Controller(su)											#0.75
	#~ c=Controller(su,(strategy.MinCellPlaceStrategy,))			#1.02
	t=time.time()
	c.run()
	t=time.time()-t
	print(t)
	if fp==1:
		print(c.hash)
	if fp==2:
		print(su)
	print(c,end='\n\n')
	return t
	
def test():
	print(sum([_run(i,2) for i in _hs]))
	
def _run1(hs):
	ans=[]
	for i in range(0,5):
		for j in range(0,5):
			su=SudokuData()
			su.setOnHashStr(hs)
			c=Controller(su,strategy_weight=[i,j,1])	
			try:
				t=time.time()
				c.run()
				t=time.time()-t
			except IndexError:
				continue
			#~ print((t,i,j))
			ans.append((t,i,j))
	ans.sort()
	print(*ans[:3])
	
def test1():
	#~ _run1('000040700031500006600037090000093025000000000950680000080310009400008630003060000')
	print([(_run1(i),i.count('0'))[1] for i in _hs])
	
def _run2(hs,ahs=None,ff=1):
	su=SudokuData()
	su.setOnHashStr(hs)
	c=Controller(su,strat,strategy_weight=[1,2,2])
	#~ c=Controller(su)
	try:
		t=time.time()
		c.run()
		t=time.time()-t
	except IndexError:
		t=100000
	if ff:
		return t
	print(t)
	return t,(1 if c.hash==ahs else 0)
	
def test2():
	hsd=[]
	for d in range(1,5):
		f=open('data/{0}.data'.format(d))
		data=f.read().split('\n')
		data=[i.split(' ')[0].strip() for i in data if i]
		#~ hsd.append(data[:20])
		hsd.append(data)
	td=[0 for d in range(4)]
	for d in range(4):
		print(d)
		td[d]=[_run2(i) for i in hsd[d]]					#001 0.11 31.46 91.41 14.45	#331 0.078 2002.24 1012.15 2006.12	#551 0.105 9.46 61.3 18.34
	print(*[(d,sum(i)) for d,i in enumerate(td)])			#001 0.17 4.94 32.2 68.8	#331 0.15 1.6 9.4 8.4
	print(sum([sum(i) for i in td]))						#001 106.12					#331 19.6
	for i in range(4):
		print(i,min(td[i]),max(td[i]))
		

def main():
	test2()

if __name__=='__main__':
	main()
