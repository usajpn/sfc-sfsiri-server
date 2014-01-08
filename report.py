#!/usr/local/bin/env python
# -*- coding: utf-8 -*-

import mechanize
import urlparse
from bs4 import BeautifulSoup as bs
import re


def report(login, pw):
    login_url = "https://vu8.sfc.keio.ac.jp/sfc-sfs/"
    term = '2013f'
    result = ""

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(login_url)
    br.select_form(nr=0)
    br.form['u_login'] = login
    br.form['u_pass'] = pw
    br.submit()

    top_url = br.response().geturl()
    params = urlparse.parse_qs(urlparse.urlparse(top_url).query)
    param_id = str(params['id']).strip('[]').strip('\'')
    timetable_url = login_url \
    + 'sfs_class/student/view_timetable.cgi?id=' + param_id \
    + '&term=' + term \
    + '&fix=1&lang=ja'

    br.open(timetable_url)
    ascii_code = unicode(br.response().read(), 'euc-jp')
    soup = bs(ascii_code)
    a_list = soup.findAll('a', {'target':'_blank'})
    class_name_list = []; class_url_list = []
    for a in a_list:
        class_name_list.append(a.string)
        class_url_list.append(a.get('href'))

    # check sata
    flag = 'student' 
    class_name_list2 = []; class_url_list2 = []
    for i in range(len(class_name_list)):
        if class_url_list[i].find(flag) != -1:
            class_name_list2.append(class_name_list[i])
            class_url_list2.append(class_url_list[i])

    for i in range(len(class_name_list2)):
        #print class_name_list2[i]

        br.open(class_url_list2[i])
        ascii_code = unicode(br.response().read(), 'euc-jp')
        source = ascii_code.encode('utf-8')
        pattern = re.compile('(<tr bgcolor="#efefef"> <th align=right valign=top nowrap><font color="#cc0000">課題\n<span class="en"><br />Assignments</span>\n\n</font></th>\n<td> \n.+<br><br>\n</td></tr>)', re.DOTALL)
        m = pattern.search(source)
        num_list = []; dl_list = []
        assignments = m.group(0).replace('\n', '')

        flag1 = '現在、登録はありません。'
        if flag1 not in assignments:
            flag2 = '<font color="red">'
            report_list = assignments.split('<!--')
            for r in report_list:
                if flag2 in r:
                    a = r.split('--> ')
                    b = a[1].split(' <a href')
                    c = b[1].split('deadline</span>: ')
                    d = c[1].split(', 提出者')
                    num_list.append(b[0]); dl_list.append(d[0])

        if len(num_list) != 0:
            result += class_name_list2[i].encode('utf-8')
            result += '<br>'
            for j in range(len(num_list)):
                result += str(num_list[j])
                result += ', '
                result += str(dl_list[j])
                result += '<br>'
                #print num_list[j] + ", " + dl_list[j]
                #print "========================="
            result += '<br>'

    return result


if __name__ == '__main__':
    result = report(login, pw)
    print result
