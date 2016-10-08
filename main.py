# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
import strategy
from sudoku import SudokuData
from strategy import Controller
import time

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
def Run():
	hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'			#0.04
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097000'			#0.002
	#~ hs='0'*81			#0.005
	s1=SudokuData()
	s1.setOnHashStr(hs)
	st=Controller(s1)
	#~ st=Controller(s1,strategy_weight=[3,3,1])
	#~ st=Controller(s1,strategy_weight=[0,0,1])
	#~ st=Controller(s1,(strategy.MinCellPlaceStrategy,))
	t=time.time()
	st.run()
	t=time.time()-t
	print(t)
	s2=SudokuData()
	s2.setOnHashStr(st.hash)
	print(s2)
	print(st)
	
Run()
