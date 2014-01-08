#!/usr/bin/python
# -*- coding:utf-8 -*-

import datetime
import time
import mechanize
import urlparse
import re
from numpy import *


def time_to_weekday(c_datetime):
	""" 0: Monday, 1: Tuesday ... """
	return c_datetime.weekday()

def time_maker(hour, minute, second):
	return datetime.time(hour, minute, second)

def period_from_time(c_time):
	period = 0

	if time_maker(9, 0, 0) <= c_time and c_time < time_maker(10, 55, 0):
		period = 1
	elif time_maker(10, 55, 0) <= c_time and c_time < time_maker(12, 40, 0):
		period = 2	
	elif time_maker(12, 40, 0) <= c_time and c_time < time_maker(14, 30, 0):
		period = 3
	elif time_maker(14, 30, 0) <= c_time and c_time < time_maker(16, 15, 0):
		period = 4
	elif time_maker(16, 15, 0) <= c_time and c_time < time_maker(18, 00, 0):
		period = 5

	return period

def parse_line(line):
	pattern = re.compile("(2013 Fall.+\d\))")
	ret = pattern.search(line)
	if not ret:
		return None
	
	return ret.group(0)

def get_day_in_num(day_str):
	""" returns day in numbers
	number is Monday:0, Tuesday:1 ... """

	ret = 0

	if day_str == 'Monday':
		ret = 0
	elif day_str == 'Tuesday':
		ret = 1
	elif day_str == 'Wednesday':
		ret = 2
	elif day_str == 'Thursday':
		ret = 3
	elif day_str == 'Friday':
		ret = 4
	elif day_str == 'Saturday':
		ret = 5
	elif day_str == 'Sunday':
		ret = 6
	
	return ret

def get_period_in_num(period_str):
	""" returns period in numbers
	period is -1 from period in real world"""	

	ret = 0

	if period_str == '1st':
		ret = 0
	elif period_str == '2nd':
		ret = 1
	elif period_str == '3rd':
		ret = 2
	elif period_str == '4th':
		ret = 3
	elif period_str == '5th':
		ret = 4

	return ret

def parse_classroom_string(classroom_str):
	pattern = re.compile("(\(\&.+\))")
	ret = pattern.search(classroom_str).group(0)
	ret = ret.replace('(&', '')
	ret = ret.replace(')', '')
	ret = ret.replace(';', ' ')
	
	return ret

def string_to_array(line):
	""" return value: [ int day, int period, string classroom ]"""
	ret = []
	day_num = 0
	split_array = line.split(' ')
	
	# for day
	day_num = get_day_in_num(split_array[3])
	ret.append(day_num)

	# for period	
	period_num = get_period_in_num(split_array[4])
	ret.append(period_num)

	# for classroom
	classroom = parse_classroom_string(split_array[5])
	ret.append(classroom)

	return ret

def array_to_matrix(timetable_array):
	""" return value: day, period, classroom"""
	ret = 5 * [ 5 * [' '] ]
	for cell_array in timetable_array:
		row = cell_array[0]
		column = cell_array[1]
		value = cell_array[2]

		ret[row][column] = value

	return ret

def fix_period( period):
	return period - 1

def get_classroom(day, period, login, pw):
	classroom = ''
	period = fix_period(period)
	
	#Browzerオブジェクトの作成
	br = mechanize.Browser()
	br.set_handle_robots(False)

	#変数login_pageの指定
	login_page = 'http://vu8.sfc.keio.ac.jp/sfc-sfs/'

	#login pageをオープン
	br.open(login_page)

	#フォームの入力
	br.select_form(nr=0)
	br["u_login"] = login
	br["u_pass"] = pw
	br.submit()

	#HTMLの取得
	br.response()

	#MY時間割をクリック
	pattern = ".*mode=1.*"
	url = br.find_link(url_regex = pattern)
	br.follow_link(url)
	br.response()

	#MY時間割テーブルのURL
	tableurl = br.find_link(url_regex = '.*sfs_class/student/view_timetable.cgi.*')
	br.follow_link(tableurl)
	br.response().read().decode("EUC-JP")

	#時間割から履修科目URLを取得し各リンクへ
	url = br.links(url_regex='.*ks=.*')

	for ul in url:
		br.follow_link(ul)
		texts = br.response().read().decode("EUC-JP")
		match = re.search(r'.*Period.*', texts)
		if match is not None:
			line = parse_line(match.group(0))
			if line is not None:
				line_array = string_to_array(line) 
				if line_array[0] == day and line_array[1]:
					classroom = line_array[2]
					break;
		br.back()

	return classroom

def classroom(day, period, login, pw):
	classroom = get_classroom(day, period, login, pw)
	
	print '[day: %s, period: %s] => classroom:%s' % (day, period, classroom)
	return classroom


if __name__ == "__main__":
	#current_datetime = datetime.datetime.now()
	#current_time = datetime.time()
	
	#day = time_to_weekday(current_datetime)
	#print 'day: %s' % day
	#period = period_from_time(current_time)
	#print 'period: %s' % period

	# test
	day = 1
	period = 0

	classroom = get_classroom(day, period)
	print classroom

	
