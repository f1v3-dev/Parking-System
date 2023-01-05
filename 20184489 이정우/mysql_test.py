#MySql
import MySQLdb
db = MySQLdb.connect("localhost","pi","1234","test")
cur = db.cursor()
d = cur.execute("select count(car_number) from numberCheck")
print(d)
