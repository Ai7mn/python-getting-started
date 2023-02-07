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
                               database="phone_link")

my_cursor = mydb.cursor(buffered=True)
sql = "SELECT * FROM phone_link where id > 1870 and  phone_id is NULL ORDER BY id ASC LIMIT 1000"

my_cursor.execute(sql)

my_results = my_cursor.fetchall()


# os.environ['HTTP_PROXY'] = "http://p.webshare.io:80:theaiman-1:theahmed"

def insert_phone_name(title, phone_id):
    insert_query = "INSERT INTO phones (the_name)  VALUES (%s)"
    insert_val = (str(title),)
    my_cursor.execute(insert_query, insert_val)
    print("done1")
    mydb.commit()
    sql = "UPDATE phone_link SET phone_id = %s WHERE id = %s"
    vals = (int(my_cursor.lastrowid), int(phone_id))
    my_cursor.execute(sql, vals)
    mydb.commit()
    print("done2")
    return str(my_cursor.lastrowid)


def insert_phone_specs(phone, spec, title, the_val):
    insert_query = "INSERT INTO phone_spec (phone, spec, title, the_val)  VALUES (%s,%s,%s,%s)"
    insert_val = (int(phone), spec, title, the_val)
    my_cursor.execute(insert_query, insert_val)
    mydb.commit()
    print("done3")


user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
    'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
    'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
    'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536',
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1',
    'Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1',
    'Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1',
    'Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Wildfire U20 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.136 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.1.1; Google Pixel Build/NMF26F; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/54.0.2840.85 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; SM-G973U Build/PPR1.180610.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Mobile Safari/537.36',
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
        break
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
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
    print(f"done : {the_url}")
