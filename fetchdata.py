import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
from lib import isInteger,progressbar


# CREATE DATABASE AND TABLE IF NECCESSARY
print('Hi!', flush=True)
conn = mysql.connector.connect(
    host='localhost', user='root', password='anm33918')
cursor = conn.cursor()
cursor.execute("SHOW DATABASES")
databases = cursor.fetchall()
if ('jadiProject',) in databases:
    cursor.execute("""USE jadiProject""")
else:
    cursor.execute("""CREATE DATABASE jadiProject""")
    cursor.execute("""USE jadiProject""")

cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
if ('houses',) not in tables:
    cursor.execute(
        """CREATE TABLE houses (price BIGINT, roomsCount SMALLINT, area SMALLINT,neighbourhood varchar(30),builtYear SMALLINT )""")
else :
    cursor.execute("TRUNCATE TABLE houses")
# READING DATA FROM WEBPAGE
prices = []
neighbourhoods = []
roomsCount = []
areas = []
builtYears = []
url = "https://shabesh.com/search/%D8%AE%D8%B1%DB%8C%D8%AF-%D9%81%D8%B1%D9%88%D8%B4/%D8%A2%D9%BE%D8%A7%D8%B1%D8%AA%D9%85%D8%A7%D9%86/%D8%AA%D9%87%D8%B1%D8%A7%D9%86?order=created_at_desc&page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

print('Reading data from shabesh website please wait!', flush=True)
for i in progressbar(range(50), "Progress: ", 40):
    response = requests.get(url + str(i), headers)
    soup = BeautifulSoup(response.content, "html.parser")
    divs = soup.find_all(
        "div", {"class": "list_infoBox__iv8WI p-2 align-self-center"})
    for div in divs:
        elements = div.select('span.px-1.font-12')
        if len(elements)!=3:
            continue
        price = div.select_one('span.list_infoItem__8EH57.list_infoPrice___aJXK.d-block')
        text = price.text.strip()
        CouldBePriceStr = text.replace(",", "").split()[0]
        if isInteger(CouldBePriceStr):
            prices.append(int(text.replace(",", "").split()[0]))
        else:
            continue
        neighbourhoods.append(str(div.select_one(
            'span[class^="list_infoItem__8EH57 ellipsis d-block"][class$="list_infoItem__8EH57 ellipsis d-block"]').contents[0]))
        areas.append(elements[0].text.split(' ')[0])
        roomsCount.append(elements[1].text.split(' ')[0])
        builtYears.append(elements[2].text.split(' ')[0])
 
insertQuery = ("INSERT INTO houses "
                "(price,roomsCount,area,neighbourhood,builtYear) "
                "VALUES (%s, %s, %s,%s,%s)")

loopRange=len(prices)
print("Inserting in database!...")
for i in progressbar(range(loopRange),"Progress: ",40):
    values=(str(prices[i]),roomsCount[i],areas[i],neighbourhoods[i],builtYears[i])
    cursor.execute(insertQuery,values)

conn.commit()
cursor.close()
conn.close()