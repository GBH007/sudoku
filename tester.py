# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
import strategy
from sudoku import SudokuData
from strategy import Controller
import time

_hs=[
	'000030002004000009000051040040320090002108300050046010030560000500000400200090000',
	'000040700031500006600037090000093025000000000950680000080310009400008630003060000',
	'006000137900600508025381009102860700600053900390702850009146075460030091013097000',
	'020003000405209000070008532102000000080000020000000304913500040000906803000300070',
	'482700100000043000300100900031000005090000030800000670003004006000370000005009312',
]

def _run(hs):
	su=SudokuData()
	su.setOnHashStr(hs)
	c=Controller(su)											#6.5	#4.6
	#~ c=Controller(su,(strategy.MinCellPlaceStrategy,))			#4.8	#1.6
	t=time.time()
	c.run()
	t=time.time()-t
	print(t)
	print(c.hash)
	print(c,end='\n\n')
	return t
	
def test():
	print(sum([_run(i) for i in _hs]))
	
def main():
	test()

if __name__=='__main__':
	main()
