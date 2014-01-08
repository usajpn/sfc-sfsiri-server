# -*- coding: utf-8
# @author usa


import mechanize
import urlparse
import time

def zanryu(building, floor, room, login, pw):
	#settings
	phone_num = '11111111111'
	parent_phone_num = '22222222222'
	
	building_num = 0
	if building == 'k':
		building_num = '1'
	elif building == 'e':
		building_num = '2'
	elif building == 'i':
		building_num = '3'
	elif building == 'o':
		building_num = '4'
	elif building == 'r':
		building_num = '5'
	elif building == 'd':
		building_num = '6'
	elif building == 't':
		building_num = '7'
	elif building == 'z':
		building_num = '8'
	elif building == 'n':
		building_num = '9'
	elif building == 'w':
		building_num = '10'
	else:
		building_num = '11'
	
	# login page url
	login_page = 'https://vu8.sfc.keio.ac.jp/sfc-sfs/'


	# make browser object
	br = mechanize.Browser()
	br.set_handle_robots(False)


	#open login page
	br.open(login_page)


	# select form
	br.select_form(nr=0)
	br['u_login'] = login
	br['u_pass'] = pw
	br.submit()


	# get top page url
	top_url = br.response().geturl()
	par = urlparse.parse_qs(urlparse.urlparse(top_url).query)


	# go to lab url
	# change ks and yc depending on your environment
	lab_url = 'https://vu9.sfc.keio.ac.jp/sfc-sfs/sfs_class/student/s_class_top.cgi?lang=ja&ks=00102&yc=2013_27341&id=' + str(par['id']).strip('[]').strip('\'')


	# go to zanryu form
	br.open(lab_url)
	br.select_form(nr=0)
	br.submit()


	# fill out zanryu form
	br.select_form(nr=0)
	br['stay_phone'] = phone_num
	br['stay_p_phone'] = parent_phone_num
	br['stay_time'] = '11:00'
	br['selectRoom'] = [building_num]
	br['selectFloor'] = [floor]
	br['stay_room_other'] = [room]
	br['stay_reason'] = 'SFC SFSiri'
	br.submit()


	print br.response().read()

if __name__ == "__main__":
	building = 'd'
	floor = 's1'
	room = '103'
	username = ''
	pw = ''

	zanryu(building, floor, room, username, pw)
