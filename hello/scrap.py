import mysql.connector
from bs4 import BeautifulSoup
import requests
from random import choice
import urllib.request
import sys
import os

mydb = mysql.connector.connect(host="188.166.2.179",
                               user="aiman",
                               password="Ayman1@1",
                               port="3306",
                               database="the_phones_db")

my_cursor = mydb.cursor(buffered=True)
sql = "SELECT * FROM phone_link where id < 1790 and phone_id is NULL ORDER BY id DESC Limit 1000"

my_cursor.execute(sql)

my_results = my_cursor.fetchall()


def insert_phone_name(title, phone_id):
    insert_query = "INSERT INTO phones (the_name)  VALUES (%s)"
    insert_val = (str(title),)
    my_cursor.execute(insert_query, insert_val)
    mydb.commit()
    sql = "UPDATE phone_link SET phone_id = %s WHERE id = %s"
    vals = (int(my_cursor.lastrowid), int(phone_id))
    my_cursor.execute(sql, vals)
    mydb.commit()
    print("done insertion phone name")
    return str(my_cursor.lastrowid)


def insert_phone_specs(phone, spec, title, the_val):
    insert_query = "INSERT INTO phone_spec (phone, spec, title, the_val)  VALUES (%s,%s,%s,%s)"
    insert_val = (int(phone), spec, title, the_val)
    my_cursor.execute(insert_query, insert_val)


user_agents = [
    'Mozilla/5.0 (Windows NT 11.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5362.133 Safari/537.36 OPR/92.0.3222.132',
    'Mozilla/5.0 (Linux; arm_64; Android 10; ART-L29N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.81.00 SA/3 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; arm_64; Android 7.1.1; OPPO A83t) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.3.87.00 SA/3 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; arm_64; Android 12; CET-LX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.81.00 SA/3 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; PCLM50) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.58 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; CMA-AN40; HMSCore 6.9.0.302) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.88 HuaweiBrowser/13.0.3.301 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5; rv:123.0esr) Gecko/20000101 Firefox/123.0esr',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2; rv:114.0) Gecko/20000101 Firefox/114.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; rv:118.0) Gecko/20110101 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0esr) Gecko/20110101 Firefox/123.0esr',
    'Mozilla/5.0 (Android 10.4; Tablet; rv:118.0) Gecko/118.0 Firefox/118.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20072806 Firefox/19.0',
    'Mozilla/5.0 (X11; Linux i686; rv:118.0esr) Gecko/20112104 Firefox/118.0esr',
    'Mozilla/5.0 (X11; U; Linux i686; tr-TR; rv:1.8.1) Gecko/20061023 SUSE/2.0-30 Firefox/2.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20062612 Firefox/25.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20062103 Firefox/23.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20091020 Linux Mint/8 (Helena) Firefox/3.5.3',
    'Mozilla/5.0 (X11; U; Linux x86_64) Gecko/20102911 Firefox/112.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4; rv:119.0) Gecko/20000101 Firefox/119.0',
    'Mozilla/5.0 (Android; Tablet; rv:121.0esr) Gecko/121.0esr Firefox/121.0esr',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:111.0) Gecko/20000101 Firefox/111.0',
    'Mozilla/5.0 (Windowxp NTG 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Windows NT.6.2; Win64; x64) Gecko/20042612 Firefox/16.0',
    'Mozilla/5.0 (X11; Linux i686; U; en; rv:1.8.0) Gecko/20060728 Firefox/1.5.0',
    'Mozilla/5.0 (X11; U; Linux x86_64) Gecko/20160609 Firefox/120.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20061708 Firefox/19.0',
    'Mozilla/5.0 () EkiohFlow/6.5.0.37816 Flow/6.5.0 (like Gecko Firefox/89.0 rv:89.0)',

]


print("start")
for x in my_results:
    print(x[2])
    print(f" id is : {x[0]} and link is : {x[2]}")
    the_url = str(x[2])
    phone_id = int(x[0])
    try:
        version = choice(user_agents)
        headers = {'User-Agent': version}
        req = urllib.request.Request(the_url, None, headers)
        page = urllib.request.urlopen(req)
    except Exception as x:
        print(f"the problem is : {x}")
        continue
    try:
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
    except Exception as x:
        print(f"the second problem is : {x}")
        continue
    try:
        phone_name = soup.find('h1').text
    except:
        phone_name = "Could not find"
    print(phone_name)
    insert_phone_name(phone_name, phone_id)
    sql = "SELECT * FROM phones ORDER BY id DESC LIMIT 1"

    my_cursor.execute(sql)

    new_phone_id = my_cursor.fetchone()
    print(str(new_phone_id[0]))
    tables = soup.find_all("table")

    for table in tables:
        header = [th.text for th in table.find_all('th')]
        try:
            the_header = str(header[0])
        except:
            the_header = "None"
        for tr in table.find_all('tr'):
            data = []
            for td in tr.find_all('td'):
                data.append(td.text)
            try:
                data1 = str(data[0])
            except:
                data1 = "None"
            try:
                data2 = str(data[1])
            except:
                data2 = "None"
            insert_phone_specs(int(new_phone_id[0]), the_header, data1, data2)
    mydb.commit()
    print(f"done : {the_url}")
