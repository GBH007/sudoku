# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

def l():
	hsd=[]
	for d in range(1,5):
		f=open('{0}.data'.format(d))
		data=f.read().split('\n')
		data=[i.split(' ')[0].strip() for i in data if i]
		hsd.append(data)
	return hsd

def analyze1(hsl):
	l=len(hsl)
	p1=sum([i.count('0') for i in hsl])/l
	p1mi=min([i.count('0') for i in hsl])
	p1ma=max([i.count('0') for i in hsl])
	print(p1,p1mi,p1ma)

for i in l():
	analyze1(i)
