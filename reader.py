# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

import re
from urllib.request import urlopen
import time
#3851
def load_p(d,n):
	data=urlopen('http://absite.ru/sudoku/{0}_{1}.html'.format(d,n)).read()
	data=re.findall(b'([\d?]{81})',data)
	if not data:
		return data
	else:
		data=[i.decode().replace('?','0') for i in data]
		return data

def m1():
	for d in range(1,5):
	#~ for d in range(1,2):
		print(d)
		f=open('f{0}.data'.format(d),'w')
		for n in range(1,3852):
		#~ for n in range(1,101):
			data=load_p(d,n)
			if data:
				print(*data,file=f)
			

m1()
