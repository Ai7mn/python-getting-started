import mysql.connector
from bs4 import BeautifulSoup
import requests
import urllib.request
import sys
import os

mydb = mysql.connector.connect(host="188.166.2.179",
                               user="aiman",
                               password="Ayman1@1",
                               port="3306",
                               database="phone_link",
                               auth_plugin='mysql_native_password')

my_cursor = mydb.cursor(buffered=True)
sql = "SELECT * FROM phone_link where phone_id is NULL ORDER BY id DESC LIMIT 60"

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


# def take(phone_id, url):
#     try:
#         page = urllib.request.urlopen(url)
#     except Exception as x:
#         print(f"the problem is : {x}")
#     soup = BeautifulSoup(page.text, 'html.parser')
#     try:
#         phone_name = soup.find('h1').text
#     except:
#         phone_name = "Could not find"
#     print(phone_name)
#
#     tables = soup.find_all("table")
#
#     for table in tables:
#         header = [th.text for th in table.find_all('th')]
#         try:
#             the_header = str(header[0])
#         except:
#             the_header = "None"
#         for tr in table.find_all('tr'):
#             data = []
#             for td in tr.find_all('td'):
#                 data.append(td.text)
#             try:
#                 data1 = str(data[0])
#             except:
#                 data1 = "None"
#             try:
#                 data2 = str(data[1])
#             except:
#                 data2 = "None"
#         insert_phone_specs(int(new_phone_id), the_header, data1, data2)
#     print(f"done : {url}")
#

print("start")
for x in my_results:
    print(x[2])
    print(f" id is : {x[0]} and link is : {x[2]}")
    the_url = str(x[2])
    phone_id = int(x[0])
    try:
        page = urllib.request.urlopen(the_url)
    except Exception as x:
        print(f"the problem is : {x}")
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
