# -*- coding: utf-8 -*-
# author:   Григорий Никониров
#           Gregoriy Nikonirov
# email:    mrgbh007@gmail.com
#

def get_miid(l):
	me=l[0]
	mi=0 if l[0]>0 else -1
	for i,e in enumerate(l):
		if 0<e and(e<me or me<=0):
			me=e
			mi=i
	return mi


