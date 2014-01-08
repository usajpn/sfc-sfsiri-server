# -*- coding: utf-8
# @author ysk


import csv

import requests
from BeautifulSoup import BeautifulSoup

import re

import mechanize, sys, traceback
from urllib2 import HTTPError
import urlparse
import time


def pe(year, month, day, sport, period, login, pw):
	#sys.setdefaultencoding('utf-8')
	# login page url
	login_page = 'https://wellness.sfc.keio.ac.jp/v3/'
	urlList = []
	
	filename = "lecture_id.csv"
	csvfile = open(filename)
	
	data = [0, 0]
	lecture_data = ""
	
	date = str(year) + "0" + str(month) + str(day)
	#sport = sport.decode('utf-8')
	#date = "20140120"
	#gen = "3"
	#shumoku = "サッカー"
	id = "0"
	
	# make browser object
	br = mechanize.Browser()
	br.set_handle_robots(False)
	
	br.open("http://google.com")
	
	try:
		#open login page
		response = br.open(login_page)
		    
	    # select form
		br.select_form(nr=0)
		br['login'] = str(login)
		br['password'] = str(pw)
	
		i = 0
		for row in csv.reader(csvfile):
			for elem in row:
				if i % 4 == 0:
					data[0] = elem
					print "data[0]", data[0], elem, date, type(str(data[0])), type(elem), type(date), date
				elif i % 4 == 1:
					data[1] = elem
					print "data[1]", data[1], elem, period, type(str(data[1])), type(elem), type(str(period)), period
				elif i % 4 == 2:
					lecture_data = elem
					#print "data[2]", lecture_data, elem, type(lecture_data), type(elem), type(str(sport.encode('utf-8'))), str(sport.encode('utf-8'))
					print "data[2]", lecture_data, elem, type(lecture_data), type(elem), type(sport.encode('utf-8'))
				elif i % 4 == 3:
					id = elem
					print "data[3]", id, elem
				i = i + 1
			else:
				#if str(data[0]) == str(date) and str(data[1]) == str(period) and str(lecture_data) == str(sport.encode('utf-8')):
				if str(data[0]) == str(date) and str(data[1]) == str(period) and str(lecture_data) == sport.encode('utf-8'):
				#if str(data[0]).encode('utf-8') == str(date).encode('utf-8') and str(data[1]).encode('utf-8') == str(period).encode('utf-8') and str(lecture_data).encode('utf-8') == str(sport).encode('utf-8'):
					print "break"
					break
#				elif str(data[0]) == 20140111:
#					print "data[0]"
#				elif str(data[1]) == str(period):
#					print "data[1]"
#				elif str(lecture_data) == str(sport):
#					print str(date), str(period), str(sport)
#					print "data[2]"
				else:
					print "continue"
					continue
				print "wbreak"
				break
	    	print
		csvfile.close()	
	
		print "youbi", data[0]
		print "id", id
	
		br.submit()
	    
	    
	    # get top page url
		top_url = br.response().geturl()
	
		for links in br.links(text_regex=u''.encode('sjis')):
			urlList.append(links.url)
	
		reserve_url = "https://wellness.sfc.keio.ac.jp" + urlList[2]
		br.open(reserve_url)
		print "reserve", reserve_url
	
		print "now: ", br.geturl()
		
	
		
		r = re.compile("(.*)(/)(.*)")
		m = r.match(reserve_url)
		print "m", m.group(1)
	
		reserve_url = m.group(1) + "/pc.php?page=reserve&mode=select&d=" + str(date) + "&semesterHidden=20135&lang=ja"
	
		br.open(reserve_url)
		print "reserve :: ", reserve_url
		print "now: ", br.geturl()
	
		print "-------"
		for form in br.forms():
			print form
		print "-------"
	
		br.select_form(nr=1)
		br['lecture'] = [str(id)]
		
		br.submit()
		print "now: ", br.geturl()
		print "-------"
		for form in br.forms():
			print form
		print "-------"
		br.select_form(nr=1)
		br.submit()
		result = br.response().read()

		return "Finish"
	
	except HTTPError, e:
	    print 'Got error code: ', e.code
	except:
	    print 'Unexpected error: ' , sys.exc_info()[0] , '\n'
	
	    # エラーの情報をsysモジュールから取得
	    info = sys.exc_info()
	    # tracebackモジュールのformat_tbメソッドで特定の書式に変換
	    tbinfo = traceback.format_tb(info[2])
	 
	    # 収集した情報を読みやすいように整形して出力する----------------------------
	    print 'Python Error.' . ljust(80, '=')
	
	    for tbi in tbinfo:
	        print tbi
	
	    print '  %s' % str(info[1])
	    print '\n' . rjust(80, '=')


if __name__ == '__main__':
	result = pe(year, month, day, sport, period, login, pw)
	print result

