# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#
from sudoku import Sudoku
import time

def fls(fname):
	return [[int(i) for i in l.split(' ') if i]for l in open(fname).read().split('\n') if l]
	
gfile=open('data.txt','a')
ans_set=set()
def run(su,d=0):
	global ans_set
	#~ if su.complete() and su.ok():
	if su.complete():
		hs=su.getHashStr()
		if not hs in ans_set:
			ans_set.add(hs)
			print(hs,file=gfile)
			print('ex')
		return 0
	n=su.getMinLostCountNum()
	#~ print(d,n,len(ans_set))
	if len(ans_set)>0:
		return 0
	if not n:
		print('nm')
		return 0
	l=su.getVarPos(n)
	for i,j in l:
		#~ print(len(su.vp[n]))
		su.set(i,j,n)
		run(su,d+1)
		su.unset(i,j)
		#~ print(len(su.vp[n]))




def Run():
	#~ hs='000040700031500006600037090000093025000000000950680000080310009400008630003060000'			#209.	#101.6			#100.7		#78.9
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097004'			#6.2	#1.8	#0.09
	hs='006000137900600508025381009102860700600053900390702850009146075460030091013097000'					#1.82	#0.1	#1.8		#1.4
	#~ hs='006000137900600508025381009102860700600053900390702850009146075460030091013097084'					#1.82	#0.02	#0.001
	s1=Sudoku()
	s1.setOnHashStr(hs)
	#~ s1.noIncPrec()
	t=time.time()
	run(s1)
	t=time.time()-t
	print(t)
	#~ print(s1.getHashNum())
	s2=Sudoku()
	s2.setOnHashStr(ans_set.pop())
	print(s2)
	
Run()
gfile.close()
