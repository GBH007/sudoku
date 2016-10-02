# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
from sudoku import Sudoku
#~ from functions import SQueue
from strategy import Strategys
import time

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
def Run():
	hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'			#209.	#101.6			#100.7		#78.9	#85		#112	#0.4
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097004'			#6.2	#1.8	#0.09
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097000'					#1.82	#0.1	#1.8		#1.4	#1.7	#2.8	#0.001
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097084'					#1.82	#0.02	#0.001
	s1=Sudoku()
	s1.setOnHashStr(hs)
	st=Strategys(s1)
	t=time.time()
	st.run()
	t=time.time()-t
	print(t)
	s2=Sudoku()
	s2.setOnHashStr(st.hasn)
	print(s2)
	print(st)
	
Run()
