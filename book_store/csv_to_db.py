import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost',user='root',passwd='1234',db='bookstore')
cursor = mydb.cursor()
csv_data = csv.reader(open('E:\PYTHON\ooks_data.csv',encoding="utf8"))
next(csv_data)
for row in csv_data:
    row = row[1:]
    cursor.execute('INSERT INTO products_data(Pid,author,title,image,quantity,price,description)''VALUES(%s,%s,%s,%s,%s,%s,%s)',row)
mydb.commit()
cursor.close()