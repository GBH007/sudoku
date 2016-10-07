# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
import strategy
from sudoku import Sudoku
#~ from functions import SQueue
from strategy import Controller
import time

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
def Run():
	hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'			#0.4
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097000'			#0.001
	s1=Sudoku()
	s1.setOnHashStr(hs)
	st=Controller(s1)
	t=time.time()
	st.run()
	t=time.time()-t
	print(t)
	s2=Sudoku()
	s2.setOnHashStr(st.hash)
	print(s2)
	print(st)
	
Run()
